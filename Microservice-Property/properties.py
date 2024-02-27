import mysql.connector
from mysql.connector import Error
from typing import List, Dict, Optional

# Database services
class PropertiesService:
    def __init__(self, db_connection):
        self.db = db_connection

    def get_properties(self, filters, limit, offset):
        cursor = self.db.cursor(dictionary=True)
        query = "SELECT * FROM properties"
        params = []

        # applying filters
        if filters is not None:
            filterlist = []
            for k, v in filters.items():
                if v:
                    # price greater than or less than filters
                    if k == "price_gt":
                        condition = "price > %s"
                        filterlist.append(condition)
                    elif k == "price_lt":
                        condition = "price < %s"
                        filterlist.append(condition)

                    # house size greater than or less than filters
                    elif k == "size_gt":
                        condition = "house_size > %s"
                        filterlist.append(condition)
                    elif k == "size_lt":
                        condition = "house_size < %s"
                        filterlist.append(condition)
                    # all other filters
                    else:
                        condition = k + " = %s"
                        filterlist.append(condition)
                    params.append(v)

            # join all filters and construct the query
            if filterlist:
                query += " WHERE " + " AND ".join(filterlist)
            
        # pagination
        if limit and offset is not None:
            query += " LIMIT %s OFFSET %s"
            params.append(limit)
            params.append(offset)

        # execute select query
        cursor.execute(query, tuple(params))
        properties = cursor.fetchall()
        cursor.close()
        return properties

    def create_property(self, property_data):
        cursor = self.db.cursor()

        # get current max id
        cursor.execute("SELECT MAX(CAST(property_id AS UNSIGNED)) FROM properties")
        max_id = cursor.fetchone()[0]
        next_id_int = 1 if max_id is None else int(max_id) + 1
        
        # padding into 10 digits
        next_id = str(next_id_int).zfill(10)

        columns = ['property_address', 'house_type', 'house_size', 'price', 'availability', 'host_id']
        values = [next_id] + [property_data.get(col) for col in columns]

        # execute insert query
        query = "INSERT INTO properties (property_id, property_address, house_type, house_size, price, availability, host_id) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(query, values)
        self.db.commit()
        cnt = cursor.rowcount
        cursor.close()
        return "Property created successfully with ID: {}".format(next_id) if cnt > 0 else "Failed to create property"


    def update_property(self, property_id, property_data):
        cursor = self.db.cursor()
        statements = []
        vals = []

        # get all update fields
        for col in property_data:
            v = property_data[col]
            if v:
                statement = col + "=%s"
                statements.append(statement)
                vals.append(v)

        query = "UPDATE properties SET " + ", ".join(statements) + " WHERE property_id=%s"
        vals.append(property_id)

        # execute update query
        cursor.execute(query, vals)
        self.db.commit()
        cnt = cursor.rowcount
        cursor.close()

        return "Property updated successfully" if cnt > 0 else "Property not found"

    def delete_property(self, property_id):
        cursor = self.db.cursor()
        query = "DELETE FROM properties WHERE property_id = %s"

        # execute delete query
        cursor.execute(query, (property_id,))
        self.db.commit()
        cnt = cursor.rowcount
        cursor.close()
        return "Property deleted successfully" if cnt > 0 else "Property not found"
