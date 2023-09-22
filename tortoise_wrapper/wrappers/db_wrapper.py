from tortoise import Tortoise
from tortoise.contrib.postgres.functions import Random

from tortoise_wrapper.constants.orm import Constant as orm_constants

from ..exceptions import BadRequestException


class ORMWrapper:
    @classmethod
    async def get_by_filters(
        cls,
        model,
        filters,
        order_by=None,
        limit=orm_constants.DEFAULT_LIMIT.value,
        offset=orm_constants.DEFAULT_OFFSET.value,
        only=None,
    ):
        """
        :param model: database model class
        :param filters: where conditions for filter
        :param order_by: for ordering on queryset
        :: Pass string value 'random' to fetch rows randomly
        :param limit: limit queryset result
        :param offset: offset queryset results
        :param only: Fetch ONLY the specified fields to create a partial model
        :return: list of model objects returned by the where clause
        """
        queryset = model.filter(**filters)
        if order_by:
            if isinstance(order_by, str):
                if order_by == "random":
                    queryset = queryset.annotate(order=Random())
                    order_by = "order"
                order_by = [order_by]
            queryset = queryset.order_by(*order_by)
        if limit:
            queryset = queryset.limit(limit)

        if offset:
            queryset = queryset.offset(offset)
        if only:
            if isinstance(only, str):
                only = [only]
            queryset = queryset.only(*only)

        return await queryset

    @classmethod
    async def update_with_filters(
        cls, row, model, payload, where_clause=None, update_fields=None
    ):
        """
        :param row: database model instance which needs to be updated
        :param model: database model class on which filters and
        update will be applied.
        Please see diff between the two.
        :param payload: values which will be updated in the database.
        :param where_clause: conditions on which update will work.
        :param update_fields: fields to update in case of model object update
        :return: None. update doesn;t return any values
        """
        if where_clause:
            await model.filter(**where_clause).update(**payload)
        else:
            for key, value in payload.items():
                setattr(row, key, value)
            await row.save(update_fields=update_fields)
        return None

    @classmethod
    async def create(cls, model, payload):
        """
        :param model: db model
        :param payload: create payload
        :return: model instance
        """
        row = await model.create(**payload)
        return row

    @classmethod
    async def bulk_create(cls, model, objects):
        """
        :param model: db model
        :param objects: list of objects to be created
        :return: model instance
        """
        row = await model.bulk_create(objects)
        return row

    @classmethod
    async def get_or_create_object(cls, model, payload, defaults=None):
        """
        :param model: database model class which needs to be get or created
        :param payload: values on which get or create will happen
        :param defaults: values on which will used to create the data which
        we do not
        want to include in filtering
        :return: model object and created - true/false
        """
        defaults = defaults or {}
        row, created = await model.get_or_create(defaults=defaults, **payload)
        return row, created

    @classmethod
    async def delete_with_filters(cls, row, model, where_clause):
        """
        :param row: model object
        :param model: db model
        :param where_clause: where conditional
        :return: None
        """
        if where_clause:
            await model.filter(**where_clause).delete()
        else:
            await row.delete()

    @classmethod
    async def raw_sql(cls, query, connection="default", values=None):
        """
        :param query: contains raw sql query which have to be executed
        :param connection: connection on which raw sql will be run
        :return:
        """
        conn = Tortoise.get_connection(connection)
        result = await conn.execute_query_dict(query, values)
        return result

    @classmethod
    async def get_by_filters_count(
        cls, model, filters, order_by=None, limit=None, offset=None
    ):
        """
        :param model: database model class
        :param filters: where conditions for filter
        :param order_by: for ordering on queryset
        :param limit: limit queryset result
        :param offset: offset queryset results
        :return: list of model objects returned by the where clause
        """
        queryset = model.filter(**filters)
        if order_by:
            queryset = queryset.order_by(order_by)
        if limit:
            queryset = queryset.limit(limit)

        if offset:
            queryset = queryset.offset(offset)

        return await queryset.count()

    @classmethod
    async def get_values_by_filters(cls, model, filters, columns):
        """
        :param model: model object
        :param filters: where conditions for filter
        :param columns: list of columns ['patient_id', 'prescription_id']
        """
        queryset = await model.filter(**filters).values(*columns)
        return queryset

    @classmethod
    async def annotate_by_filters(
        cls,
        model,
        filters,
        column,
        function,
        group_by=None,
        order_by=None,
        values=None,
    ):
        """
        :param model: model object
        :param filters: where conditions for filter
        :param column: The column which need for annotate
        :param function: Max/Min/Count (max, count)
        :param order_by: for ordering on queryset
        :param group_by: for grouping on queryset
        :param values: list of columns ['patient_id', 'prescription_id']
        """
        if not values:
            values = []

        try:
            agg_col_name = function.__name__.lower()
        except (TypeError, ValueError, AttributeError) as ex:
            raise BadRequestException(f"Invalid function name: {function}") from ex

        values.append(agg_col_name)
        queryset = (
            model.annotate(**{agg_col_name: function(column)})
            .filter(**filters)
            .group_by(group_by)
        )
        if order_by:
            queryset = queryset.order_by(order_by)
        queryset = await queryset.values(*values)
        return queryset

    @classmethod
    async def raw_sql_script(cls, query, connection="default"):
        """
        :param query: contains raw sql query with multiple statements
        which have to be executed
        :param connection: connection on which raw sql will be run
        :return:
        """
        conn = Tortoise.get_connection(connection)
        await conn.execute_script(query)
