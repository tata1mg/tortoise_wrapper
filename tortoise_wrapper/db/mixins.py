from datetime import date, datetime

from asyncpg.pgproto.pgproto import UUID  # pylint: disable=E0611
from tortoise import Model
from tortoise.exceptions import NoValuesFetched


class ModelUtilMixin:
    async def to_dict(
        self: Model, filter_keys=None, get_related=True, related_fields=None
    ):
        """

        :param filter_keys: Any Specific Keys which required in the
        Dictionary Object,
        if not mentioned, all the Model values will be added to the
        Dictionary Object.
        :param get_related:  If related Objects need to be fetched,
        set this params.
        :param related_fields:  get_related is True, then specify the
        fields, If it is None, we get all the related Fields.
        :return:  Serializable Dictionary
        """

        serializable_types = [
            str,
            int,
            list,
            tuple,
            dict,
            bool,
            set,
            type(None),
            float,
            UUID,
            datetime,
            date,
        ]
        result = {}

        # Get all the FK, One2One and Reverse FK filed sets.
        fk_fields = self._meta.fk_fields
        o2o_fields = self._meta.o2o_fields
        fk_o2o_fields = list(set(fk_fields) | set(o2o_fields))
        backward_fk_fields = self._meta.backward_fk_fields
        related_fields = related_fields or list(
            set(backward_fk_fields) | set(fk_o2o_fields)
        )

        # If no Filter Keys are given, all the variables of the Model class
        # will be taken in account.
        if not filter_keys:
            filter_keys = (
                getattr(self, "serializable_keys", None) or self._meta.fields_map.keys()
            )

        for key in filter_keys:
            is_fk = key in backward_fk_fields
            is_related = key in related_fields
            if get_related and is_fk and is_related:
                bk_relational_data = []
                try:
                    related_data = await getattr(self, key).all()
                except NoValuesFetched as exception:
                    print(exception)
                    await self.fetch_related(key)
                    related_data = await getattr(self, key).all()
                for obj in related_data:
                    obj_dict = await obj.to_dict(get_related=False)
                    if obj_dict:
                        bk_relational_data.append(obj_dict)
                result[key] = bk_relational_data
            else:
                result[key] = getattr(self, key, None)

            if get_related and key in fk_o2o_fields and key in related_fields:
                relational_key = "_" + key
                if not hasattr(self, relational_key):
                    await self.fetch_related(key)
                obj = getattr(self, key, None)
                result[key] = await obj.to_dict(get_related=False) if obj else None

            if not type(result.get(key, None)) in serializable_types:
                del result[key]

        return result
