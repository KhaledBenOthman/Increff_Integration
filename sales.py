from decouple import config
import pyodbc

connection_string = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={config('SERVER')};DATABASE={config('DATABASE')};UID={config('UNAME')};PWD={config('PW')};encrypt=no;"

class Sales:
    channel: str
    storeId: id
    itemLookupCode: str
    size: str
    color: str
    styleColor:str
    isGrandTotalRowTotal: str
    dateSold: str
    sumQtySold: float
    sumRevenue: float
    discountValue: float
    itemStatus: str

    def __init__(self, channel, storeId, itemLookupCode, size, color, isGrandTotalRowTotal, dateSold,
                 sumQtySold, sumRevenue, discountValue, itemStatus, styleColor):
        self.channel = channel
        self.storeId = storeId
        self.size = size
        self.styleColor = styleColor
        self.dateSold = dateSold
        self.itemLookupCode = itemLookupCode
        self.itemStatus = itemStatus
        self.color = color
        self.isGrandTotalRowTotal = isGrandTotalRowTotal
        self.sumQtySold = sumQtySold
        self.sumRevenue = sumRevenue
        self.discountValue = discountValue




    @staticmethod
    def get_sales_per_store():

        sales_list = []
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()

        SQL_QUERY = f""" select
            case when store.Zip ='Franchise' then 'Franchise'
			when store.Zip ='Outlet' then 'Outlet' 
			when store.Zip ='E-Commerce' then 'E-Commerce' 
			else 'Carina Stores' end
			  as Channel,
            te.StoreID as [;Store ID],
            item.ItemLookupCode,
            itemclasscomponent.Detail2 as [Size],
            itemclasscomponent.Detail1 as [Color],
            'FALSE' as [IsGrandTotalRowTotal],
            [Transaction].[Time] as [Date_Sold],
            te.quantity as [SumQty_Sold],
            te.price * te.quantity as [SumRevenue],
            ((te.fullprice * te.quantity)-(te.price * te.quantity)) as [Discount_Value],
             case when item.Inactive = 1 then 'Inactive' else 'Active' end as [ItemStatus]
            from transactionentry as te
            inner join item on te.itemid = item.ID
            inner join ItemClassComponent on item.id = ItemClassComponent.ItemID
			inner join Store on te.StoreID = store.ID
            --inner join [Stores_INCRAFF] as s on te.StoreID = s.id
            inner join [transaction] on te.transactionnumber = [transaction].transactionnumber and te.storeid = [transaction].storeid
            where convert(date,[transaction].[Time]) between convert(date,getdate()-14) and convert(date,getdate()-1)
             order by [Transaction].[Time] desc

            """


        cursor.execute(SQL_QUERY)

        for row in cursor.fetchall():
            item = row[2]
            size = row[3]
            styleColor = item.replace(f'-{size}', '')
            sales = Sales(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9]
                          , row[10], styleColor)

            sales_list.append(sales.__dict__)

        # records = cursor.fetchall()
        #
        # data_list = []
        # for r in records:
        #     record_list = list(r)
        #     data_list.append(record_list)

        cursor.close()
        conn.close()

        return sales_list
