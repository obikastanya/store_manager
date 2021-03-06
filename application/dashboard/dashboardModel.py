from app import db

class Dashboard:
    # we use raw query instead of orm because its more flexible and easy to modified.
    def getSummaryOfTotal(self,param):
        query="""
        select * from ( 
        select sum(coalesce(th_total_price,0)) as total_cash_out,
        count(th_id) as total_transaction_product_sold  
        from transaction_sold_head 
        where extract(year from th_date) = :date_year) as product_sold,
        (
        select sum(coalesce(tp_nominal)) as total_cash_in,
        count(tp_id) as total_transaction_product_purchased 
        from transaction_purchased_head 
        where extract(year from tp_date)= :date_year
        ) as product_purchased,
        (
        select 
        sum(coalesce(mss_warehouse_stock,0))
        +
        sum(coalesce( mss_store_stock,0)) as total_product_in_store
        from ms_stock
        ) as availability_stock
        """
        return db.session.execute(query, param).first()

    def getSummaryOfPurchasedVsSoldInMonth(self, param):
        query="""
        select  
        num as date_sold, 
        coalesce(total_sold,0) as total_sold, 
        coalesce(total_purchased,0) as total_purchased
        from (
            select generate_series(1, :number_date_in_month ) 
            as num
        ) as date_number 

        left join (
            select 
            extract(day from th_date) as sold_date, 
            sum(th_total_price) as total_sold 
            from transaction_sold_head 
            where extract(year from th_date)= :date_year
            and extract(month from th_date)= :date_month
            group by th_date, extract(day from th_date)
        ) as transaction_sold

        on date_number.num =transaction_sold.sold_date

        left join (
            select 
            extract(day from tp_date) as purchased_date, 
            sum(tp_nominal) as total_purchased 
            from transaction_purchased_head 
            where extract(year from tp_date)= :date_year 
            and extract(month from tp_date)= :date_month
            group by tp_date, extract(day from tp_date)
        ) as transaction_purchased
        on date_number.num =transaction_purchased.purchased_date
        """
        return db.session.execute(query, param).all()

    def getSummaryOfPurchasedVsSoldInYear(self, param):
        query="""
        select  
        num as date_sold, 
        coalesce(total_sold,0) as total_sold, 
        coalesce(total_purchased,0) as total_purchased
        from (
            select generate_series(1, :number_date_in_month) 
            as num
        ) as date_number 

        left join (
            select 
            extract(month from th_date) as sold_date, 
            sum(th_total_price) as total_sold 
            from transaction_sold_head 
            where extract(year from th_date)= :date_year
            group by  extract(month from th_date)
        ) as transaction_sold

        on date_number.num =transaction_sold.sold_date

        left join (
            select 
            extract(month from tp_date) as purchased_date, 
            sum(tp_nominal) as total_purchased 
            from transaction_purchased_head 
            where extract(year from tp_date)= :date_year
            group by tp_date, extract(month from tp_date)
        ) as transaction_purchased
        on date_number.num =transaction_purchased.purchased_date
        """
        return db.session.execute(query, param).all()

    def getSummaryOfPurchasedVsSoldGroupByCategoryInMonth(self, param):
        query="""
        select
        msc_desc,
        sum(coalesce(td_on_sale_price,0)* coalesce(td_quantity,0))
        from ms_product
        join ms_category
        on msp_msc_id = msc_id 
        join
        (
        select th_id,td_msp_id, td_on_sale_price, td_quantity from transaction_sold_head 
        join transaction_sold_detail
        on th_id=td_th_id and extract(year from th_date)= :date_year
            and extract(month from th_date)= :date_month
        ) as transaction_sold
        on transaction_sold.td_msp_id =msp_id
        group by msc_desc
        """
        return db.session.execute(query,param).all()

    def getSummaryOfPurchasedVsSoldGroupByCategoryInYear(self, param):
        query="""
        select
        msc_desc,
        sum(coalesce(td_on_sale_price,0)* coalesce(td_quantity,0))
        from ms_product
        join ms_category
        on msp_msc_id = msc_id 
        join
        (
        select th_id,td_msp_id, td_on_sale_price, td_quantity from transaction_sold_head 
        join transaction_sold_detail
        on th_id=td_th_id and extract(year from th_date)= :date_year
        ) as transaction_sold
        on transaction_sold.td_msp_id =msp_id
        group by msc_desc
        """
        return db.session.execute(query,param).all()

    def getSummaryOfSoldInMonth(self, param):
        query="""
        select  
        num as date_sold, 
        coalesce(total_transaction_sold,0) as total_transaction_sold
        from (
            select generate_series(1, :number_date_in_month ) 
            as num
        ) as date_number 
        left join (
            select 
            extract(day from th_date) as sold_date, 
            count(th_id) as total_transaction_sold 
            from transaction_sold_head 
            where extract(year from th_date)= :date_year
			and extract(month from th_date)= :date_month
            group by extract(day from th_date)
        ) as transaction_sold
        on date_number.num =transaction_sold.sold_date
        """
        return db.session.execute(query,param).all()

    def getSummaryOfSoldInYear(self, param):
        query="""
        select  
        num as date_sold, 
        coalesce(total_transaction_sold,0) as total_transaction_sold
        from (
            select generate_series(1, :number_date_in_month ) 
            as num
        ) as date_number 
        left join (
            select 
            extract(month from th_date) as sold_date, 
            count(th_id) as total_transaction_sold 
            from transaction_sold_head 
            where extract(year from th_date)= :date_year
            group by extract(month from th_date)
        ) as transaction_sold
        on date_number.num =transaction_sold.sold_date
        """
        return db.session.execute(query,param).all()

    def getSummaryOfSoldGroupByCategoryInMonth(self, param):
        query="""
        select
        msc_desc,
        count(th_id) 
        from ms_product
        join ms_category
        on msp_msc_id = msc_id 
        join
        (
        select th_id,td_msp_id from transaction_sold_head 
        join transaction_sold_detail
        on th_id=td_th_id and extract(year from th_date)= :date_year
        and extract(month from th_date)= :date_month
        ) as transaction_sold
        on transaction_sold.td_msp_id =msp_id
		group by msc_desc
        """
        return db.session.execute(query,param).all()

    def getSummaryOfSoldGroupByCategoryInYear(self, param):
        query="""
        select
        msc_desc,
        count(th_id)
        from ms_product
        join ms_category
        on msp_msc_id = msc_id 
        join
        (
        select th_id,td_msp_id from transaction_sold_head 
        join transaction_sold_detail
        on th_id=td_th_id and extract(year from th_date)= :date_year
        ) as transaction_sold
        on transaction_sold.td_msp_id =msp_id
		group by msc_desc
        """
        return db.session.execute(query,param).all()


    # wip
    def getSummaryOfPurchasedInMonth(self, param):
        query="""
        select  
        num as date_purchased, 
        coalesce(total_transaction_purchased,0) as total_transaction_purchased
        from (
            select generate_series(1, :number_date_in_month) 
            as num
        ) as date_number 
        left join (
            select 
            extract(day from tp_date) as purchased_date, 
            count(tp_id) as total_transaction_purchased 
            from transaction_purchased_head 
            where extract(year from tp_date)= :date_year
			and extract(month from tp_date)= :date_month
            group by extract(day from tp_date)
        ) as transaction_purchased
        on date_number.num =transaction_purchased.purchased_date
        """
        return db.session.execute(query,param).all()

    def getSummaryOfPurchasedInYear(self, param):
        query="""
		select  
        num as date_purchased, 
        coalesce(total_transaction_purchased,0) as total_transaction_purchased
        from (
            select generate_series(1,  :number_date_in_month ) 
            as num
        ) as date_number 
        left join (
            select 
            extract(month from tp_date) as purchased_date, 
            count(tp_id) as total_transaction_purchased 
            from transaction_purchased_head 
            where extract(year from tp_date)= :date_year
            group by extract(month from tp_date)
        ) as transaction_purchased
        on date_number.num =transaction_purchased.purchased_date
        """
        return db.session.execute(query,param).all()

    def getSummaryOfPurchasedGroupByCategoryInMonth(self, param):
        query="""
        select
        msc_desc,
        count(tp_id)
        from ms_product
        join ms_category
        on msp_msc_id = msc_id 
        join
        (
        select tp_id,tpd_msp_id from transaction_purchased_head 
        join transaction_purchased_detail
        on tp_id=tpd_tp_id and extract(year from tp_date)= :date_year
        and extract(month from tp_date)= :date_month
        ) as transaction_purchased
        on transaction_purchased.tpd_msp_id =msp_id
		group by msc_desc
        """
        return db.session.execute(query,param).all()
        
    def getSummaryOfPurchasedGroupByCategoryInYear(self, param):
        query="""
        select
        msc_desc,
        count(tp_id)
        from ms_product
        join ms_category
        on msp_msc_id = msc_id 
        join
        (
        select tp_id,tpd_msp_id from transaction_purchased_head 
        join transaction_purchased_detail
        on tp_id=tpd_tp_id and extract(year from tp_date)= :date_year
        ) as transaction_purchased
        on transaction_purchased.tpd_msp_id =msp_id
		group by msc_desc
        """
        return db.session.execute(query,param).all()
    
    def getSummaryOfAvailabilityStore(self):
        query="""
        select 
		msc_desc,
		sum(coalesce( mss_store_stock,0)) as total_product_in_store
        from ms_stock
		join ms_product
		on mss_msp_id=msp_id
		join ms_category
		on msp_msc_id=msc_id
		group by msc_desc
        """
        return db.session.execute(query).all()

    def getSummaryOfAvailabilityWarehouse(self):
        query="""
        select 
		msc_desc,
		sum(coalesce(mss_warehouse_stock,0)) as total_product_in_warehouse
        from ms_stock
		join ms_product
		on mss_msp_id=msp_id
		join ms_category
		on msp_msc_id=msc_id
		group by msc_desc
        """
        return db.session.execute(query).all()