from decouple import config
import pyodbc

connection_string = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={config('SERVER')};DATABASE={config('DATABASE')};UID={config('UNAME')};PWD={config('PW')};encrypt=no;"


class Inventory:
    channel: str
    storeId: id
    storeName: str
    itemLookupCode: str
    qtyOnHand: float
    lastCheckDate: str
    mostRecentQtyUpdate: str
    itemStatus: str
    styleColor: str
    isGrandTotalRowTotal: str

    def __init__(self, channel, storeId, storeName, itemLookupCode, qtyOnHand, lastCheckDate, mostRecentQtyUpdate, itemStatus, styleColor,  isGrandTotalRowTotal):
        self.channel = channel
        self.storeName = storeName
        self.itemLookupCode = itemLookupCode
        self.storeId = storeId
        self.styleColor = styleColor
        self.lastCheckDate = lastCheckDate
        self.mostRecentQtyUpdate = mostRecentQtyUpdate
        self.itemStatus = itemStatus
        self.isGrandTotalRowTotal = isGrandTotalRowTotal
        self.qtyOnHand = qtyOnHand


    @staticmethod
    def get_inventory_per_store():
        inventory_list = []
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()

        SQL_QUERY = f""" select
             case when s.Zip ='Franchise' then 'Franchise'
			when s.Zip ='Outlet' then 'Outlet' 
			when s.Zip ='E-Commerce' then 'E-Commerce' 
			else 'Carina Stores' end
			 as Channel,
            StoreID as [;Store ID],
            s.[name] as [Store_Name],
            item.ItemLookupCode,
            itemdynamic.SnapShotQuantity as [Qty OH],
            getdate() as [Last_Check_Date],
            convert(date,snapshottime) as [MostRecentQtyUpdate],
             case when item.Inactive = 1 then 'Inactive' else 'Active' end as [ItemStatus],
			 itemclasscomponent.Detail2 as [Size]
            from ItemDynamic
            inner join item on ItemDynamic.itemid = item.ID
            inner join [Stores_INCRAFF] as s on ItemDynamic.StoreID = s.id
			inner join ItemClassComponent on item.id = ItemClassComponent.ItemID
            where itemdynamic.SnapShotQuantity <> 0
        """

        cursor.execute(SQL_QUERY)

        for row in cursor.fetchall():
            item = row[2]
            size = row[8]
            styleColor = item.replace(f'-{size}', '')
            inventory = Inventory(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], styleColor , 'FALSE')
            inventory_list.append(inventory.__dict__)

        cursor.close()
        conn.close()

        return inventory_list
