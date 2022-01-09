class DatatableProductSoldImpl extends BaseDatatable {
    constructor() {
        super()
        this.tableColumns = [
            {
                data: null,
                defaultContent: ''
            },
            {
                data: 'transaction_id'
            },
            {
                data: 'transaction_date'
            },
            {
                data: 'employee_transaction',
                render: ( data ) => {
                    return data.name

                }
            },
            {
                data: 'payment_method',
                render: ( data ) => {
                    return data.payment_method

                }
            },
            {
                data: 'total_price'
            },
            {
                data: 'tax'
            },
            {
                data: 'paid'
            },
            {
                data: 'change'
            },
            {
                data: null,
                render: ( data ) => {
                    const buttonDetail = `<button type="button" class="btn btn-warning btn-detail-data" value=${ data.transaction_id } onclick="new ModalForm().showModal('id_modal_for_detail_data')">Detail</button>`
                    return buttonDetail + '&nbsp;' + this.buttonDelete.replace( "_data_", data.transaction_id )
                }
            }
        ]
        this.columnName = [
            { "name": "no", "targets": 0 },
            { "name": "transaction_id", "targets": 1 },
            { "name": "transaction_date", "targets": 2 },
            { "name": "cashier", "targets": 3 },
            { "name": "payment_method", "targets": 4 },
            { "name": "total_price", "targets": 5 },
            { "name": "tax", "targets": 6 },
            { "name": "paid", "targets": 7 },
            { "name": "change", "targets": 8 },
            { "name": "action", "targets": 9 }
        ]
        this.datatableId = '#product_sold_transaction_datatable_id'
        this.apiEndpoint = '/product_sold_api'
    }
    getTableSetup() {
        const getDataFromFields = ( id ) => {
            try {
                const value = document.querySelector( id ).value
                return value
            }
            catch ( e ) {
                return null
            }
        }
        const tableSetup = {
            ajax: {
                url: this.apiEndpoint,
                method: 'GET',
                data: ( data ) => {
                    data.product_id = getDataFromFields( '#productFields' )
                    data.discount_id = getDataFromFields( '#discountFields' )
                    data.cashier_id = getDataFromFields( '#cashierFields' )
                    data.transaction_date = getDataFromFields( '#transactionDateFields' )
                }
            },
            scrollX: true,
            language: {
                searchPlaceholder: "Search transaction code"
            },

            processing: true,
            serverSide: true,
            columns: this.tableColumns,
            columnDefs: this.columnName,
            order: [ [ 1, 'asc' ] ],
            dom: this.toolbarDomConfig.top + this.toolbarDomConfig.table + this.toolbarDomConfig.bottom,
            fnInitComplete: () => {
                //Set button create new data for toolbar
                $( 'div.toolbar' ).html( this.buttonCreateNewData )
            }
        }
        return tableSetup
    }
    bindEventForActionsButton( datatableInstance ) {
        datatableInstance.on( 'click', '.btn-detail-data', function ( e ) {
            new AjaxImpl().getSingleData( e.target.value )
        } )
        datatableInstance.on( 'click', this.btnClassDeleteData, ( e ) => {
            new ModalFormImpl().setDeleteConfirmMessage( e.target.value )
        } )
    }
    initiateDatatableForTransactionChart() {
        const tableCashierSettings = {
            scrollX: true,
            deferRender: true,
            columns: [
                {
                    data: 'no',
                    defaultContent: ''
                },
                { data: 'product_id' },
                { data: 'product_desc' },
                {
                    data: 'quantity'
                },
                {
                    data: 'price'
                },
                {
                    data: 'sub_total'
                },
                {
                    data: 'cutt_off'
                },
                {
                    data: 'discount_applied', render: ( productRecord ) => {
                        return new FormDataImpl().getDiscountNamesForCashier( productRecord.discount_applied_on_product ).discount_master
                    }
                },
                {
                    data: 'btnRemove',
                    default: ''
                }
            ]
        }
        const tableCashier = $( '#product_sold_cart_datatable_id' ).DataTable( tableCashierSettings )
        tableCashier.on( 'draw.dt order.dt search.dt', function () {
            tableCashier.column( 0, { search: 'applied', order: 'applied' } ).nodes().each( function ( cell, i ) {
                cell.innerHTML = i + 1;
            } );
        } ).draw();
        $( '#product_sold_cart_datatable_id' ).on( 'click', '.btn-remove-data', function () {
            const table = $( '#product_sold_cart_datatable_id' ).DataTable()
            table.row( $( this ).parents( 'tr' ) ).remove().draw();
            new ButtonEventImpl().hideDetailCheckout()
            new ButtonEventImpl().resetDetailCheckout()
        } )
        $( '#product_sold_cart_datatable_id' ).on( 'input', '.quantityFields', function ( event ) {
            if ( !this.value ) return;
            let newQuantity = parseInt( this.value )
            if ( newQuantity < 1 ) newQuantity = 1;

            const table = $( '#product_sold_cart_datatable_id' ).DataTable()
            let currentRowData = table.row( $( this ).parents( 'tr' ) ).data()
            let newRowData = { ...currentRowData }

            newRowData.sub_total = currentRowData.price * newQuantity
            newRowData.quantity = new FormDataImpl().getQuantityTemplate( newRowData, newQuantity )
            newRowData.cutt_off = new FormDataImpl().getCuttOffTemplate( newRowData.productRecord, newQuantity )
            table.row( $( this ).parents( 'tr' ) ).data( newRowData ).invalidate().draw()

        } )
    }
    clearCashierTable() {
        let table = $( '#product_sold_cart_datatable_id' ).DataTable();
        table.clear().draw();
    }
}

class FormDataImpl extends FormData {
    constructor() {
        super()
    }
    getAddNewDataFormValues() {
        let formValues = {
            product_id: document.querySelector( '#productIdFields' ).value,
            discount_id: document.querySelector( '#discountIdFields' ).value,
            start_date: document.querySelector( '#startDateFields' ).value,
            expired_date: document.querySelector( '#expiredDateFields' ).value
        }
        return formValues
    }
    getDeleteFormValues() {
        let formValues = {
            transaction_id: document.getElementById( 'delete_confirm_massage_id' ).value
        }
        return formValues
    }
    getUpdateFormValues() {
        let formValues = {
            product_id: document.querySelector( '#productIdUpdateFields' ).value,
            discount_id: document.querySelector( '#discountIdUpdateFields' ).value,
            start_date: document.querySelector( '#startDateUpdateFields' ).value,
            expired_date: document.querySelector( '#expiredDateUpdateFields' ).value,
            active_status: this.getActiveStatusValue( '#activeStatusFields' )
        }
        return formValues
    }
    setUpdateFormValues( recordValues ) {
        document.querySelector( '#productIdUpdateFields' ).value = recordValues.discount_product.product_id
        document.querySelector( '#discountIdUpdateFields' ).value = recordValues.discount_master.discount_id
        document.querySelector( '#startDateUpdateFields' ).value = recordValues.start_date
        document.querySelector( '#expiredDateUpdateFields' ).value = recordValues.expired_date
        document.querySelector( '#activeStatusFields' ).checked = recordValues.active_status
        document.querySelector( '#activeStatusFields' ).value = recordValues.active_status
    }
    generateRow( record ) {
        const replaceEmpty = ( value ) => {
            if ( value ) return value
            if ( value === 0 ) return value;
            return '-';
        }
        let rowRecord = `<tr>
                            <td>${ replaceEmpty( record.index + 1 ) }</td>
                            <td>${ replaceEmpty( record.product.product_id ) }</td>
                            <td>${ replaceEmpty( record.product.product_desc ) }</td>
                            <td>${ replaceEmpty( record.quantity ) }</td>
                            <td>${ replaceEmpty( record.saled_price ) }</td>
                            <td>${ replaceEmpty( record.quantity * record.saled_price ) }</td>
                            <td>${ replaceEmpty( this.getCuttOff( record.detail_discount_applied ) ) }</td>
                            <td>${ replaceEmpty( this.getDiscountNames( record.detail_discount_applied ) ) }</td>
                        </tr>`
        return rowRecord
    }

    getDiscountNamesForCashier( discountAppliedOnProduct ) {
        let discountMaster = []
        let discountNominal = 0

        for ( const discount of discountAppliedOnProduct ) {
            discountMaster.push( discount.discount_master.desc )
            discountNominal += discount.discount_master.discount_nominal
        }

        return { discount_master: discountMaster.join( ", " ), discount_nominal: discountNominal }
    }
    getQuantityTemplate( productRecord, defaultQuantity = 1 ) {
        let inputQuantity = `<div ><input id='input_for_quantity_' type="number" class="form-control text-center quantityFields" value=${ defaultQuantity }></div>`
        return inputQuantity.replace( 'input_for_quantity_', 'input_for_quantity_' + productRecord.product_id )
    }
    getCuttOffTemplate( productRecord, defaultQuantity = 1 ) {
        return new FormDataImpl().getDiscountNamesForCashier( productRecord.discount_applied_on_product ).discount_nominal * defaultQuantity
    }
    addItemToCashierTable( productRecord ) {
        let removeRecordBtn = `<div class='text-center'><button type="button" class="btn btn-danger btn-remove-data" >X</button></div>`
        let records = {
            no: '',
            product_id: productRecord.product_id,
            product_desc: productRecord.product_desc,
            price: productRecord.price,
            quantity: this.getQuantityTemplate( productRecord ),
            sub_total: productRecord.price * 1,
            cutt_off: this.getCuttOffTemplate( productRecord ),
            discount_applied: productRecord,
            productRecord: productRecord,
            btnRemove: removeRecordBtn
        }
        new ModalFormImpl().addCashierTableRows( [ records ] )
    }

    setDetailModalTables( recordValues ) {
        let tableContent = ""
        for ( let [ index, record ] of recordValues.entries() ) {
            record.index = index
            tableContent += this.generateRow( record )
        }
        let table = document.querySelector( '#product_sold_detail_transaction_datatable_id > tbody' )
        table.innerHTML = tableContent
    }
    generateOption( recordValues ) {
        let options = ''
        for ( const values of recordValues ) {
            options += ` <option value=${ values.id }>${ values.description }</option> `
        }
        return options
    }
    setOptionForSelectFields( elementsToSet, recordValues ) {
        // some dom manipulation
        for ( const id of elementsToSet ) {
            const options = this.generateOption( recordValues )
            document.querySelector( id ).innerHTML = ''
            document.querySelector( id ).innerHTML = options
        }
    }
    getCuttOff( discountApplied ) {
        let cuttOff = 0
        for ( const discount of discountApplied ) {
            cuttOff += discount.cutt_off_nominal
        }
        return cuttOff
    }
    getDiscountNames( discountApplied ) {
        let discountNames = []
        for ( const discount of discountApplied ) {
            discountNames.push( discount.discount_applied.discount_master.desc )
        }
        return discountNames.join( ", " )
    }
}
class FormValidationImpl extends FormValidation {
    constructor() {
        super()
    }
    validateUpdateParams( updateParams ) {
        const validIdProduct = this.validateIdProduct( updateParams )
        const validIdDiscount = this.validateIdDiscount( updateParams )
        const validStartDate = this.validateStartDate( updateParams )
        const validExpiredDate = this.validateExpiredDate( updateParams )
        const validActiveStatus = this.validateActiveStatus( updateParams )

        if ( !validIdProduct.isValid ) return validIdProduct;
        if ( !validIdDiscount.isValid ) return validIdDiscount;
        if ( !validStartDate.isValid ) return validStartDate;
        if ( !validExpiredDate.isValid ) return validExpiredDate;
        if ( !validActiveStatus.isValid ) return validActiveStatus;
        return this.validateResult( 'Data is valid', true )
    }
    validateDeleteParams( deleteParams ) {
        const validTransactionId = this.validateTransactionId( deleteParams )
        if ( !validTransactionId.isValid ) return validTransactionId;
        return this.validateResult( 'Data is valid', true )
    }
    validateInsertParams( insertParams ) {
        return this.validateResult( 'Data is valid', true )
    }
    validateTransactionId( formData ) {
        if ( isNaN( formData.transaction_id ) ) {
            return this.validateResult( 'Invalid transaction selected' )
        }
        if ( !( parseInt( formData.transaction_id ) ) ) {
            return this.validateResult( 'Invalid transaction selected' )
        }
        return this.validateResult( 'Data is valid', true )
    }
    validateIdDiscount( formData ) {
        if ( isNaN( formData.discount_id ) ) {
            return this.validateResult( 'Invalid master discount selected' )
        }
        if ( !( parseInt( formData.product_id ) ) ) {
            return this.validateResult( 'Invalid Product selected' )
        }
        return this.validateResult( 'Data is valid', true )
    }
    validateStartDate( formData ) {
        if ( !formData.start_date ) {
            return this.validateResult( 'Start date is empty' )
        }
        return this.validateResult( 'Data is valid', true )
    }
    validateExpiredDate( formData ) {
        if ( !formData.expired_date ) {
            return this.validateResult( 'Expired date is empty' )
        }
        return this.validateResult( 'Data is valid', true )
    }
    validateActiveStatus( formData ) {
        const isValidStatus = [ 'Y', 'N' ].includes( formData.active_status )
        if ( !isValidStatus ) {
            return this.validateResult( 'Active status value is invalid' )
        }
        return this.validateResult( 'Data is valid', true )
    }
    validateResult( message = '', isValid = false ) {
        return { isValid: isValid, message: message }
    }
}
class ModalFormImpl extends ModalForm {
    constructor() {
        super()
    }
    createSelectFields() {
        $( '.selectForm' ).selectize( {
            sortField: 'text',
            create: false
        } );
        $( '#productInputFields' ).selectize( {
            sortField: 'text',
            create: false,
            onChange: ( productId ) => {
                if ( !productId ) return;
                $( "#productInputFields" )[ 0 ].selectize.clear();

                if ( new ButtonEventImpl().isExistInCashierTable( productId ) ) {
                    new ModalFormImpl().increaseProductQuantity( productId )
                    return
                }
                new AjaxImpl().getSingleProduct( productId )
            }
        } );
    }
    increaseProductQuantity( productId ) {
        let quantityField = document.querySelector( `#input_for_quantity_${ productId }` )
        let oldQuantity = quantityField.value
        quantityField.value = parseInt( oldQuantity ) + 1
        $( `#input_for_quantity_${ productId }.quantityFields` ).trigger( 'input' )
    }
    bindEventToFormFilterAndNewTransaction() {
        const btnFilterData = document.querySelector( '.btn-filter-product-sold' )
        const btnCheckout = document.querySelector( '.btn-checkout-product-sold' )

        btnFilterData.addEventListener( 'click', () => {
            new DatatableProductSoldImpl().reloadDatatable()
        } )
        btnCheckout.addEventListener( 'click', () => {
            new ButtonEventImpl().checkOutTransaction()
        } )

        // calculate change everytime paid changes
        const paidField = document.querySelector( '#paidFields' )
        paidField.addEventListener( 'input', ( event ) => {
            new ModalFormImpl().setChangeOfTransaction( event.target.value )
        } )

        const payTransaction = document.querySelector( '.btn-pay-product-sold' )
        payTransaction.addEventListener( 'click', () => {
            new ButtonEventImpl().saveNewTransaction()
        } )

    }
    setChangeOfTransaction( paidValue ) {
        let netPrice = document.querySelector( '#netPriceFields' ).textContent;
        let tax = document.querySelector( '#taxFields' ).textContent;
        let cuttOff = document.querySelector( '#cuttOffFields' ).textContent;
        let totalPriceToPaid = ( parseInt( netPrice ) - parseInt( cuttOff ) ) + parseInt( tax )
        let change = paidValue - totalPriceToPaid
        document.querySelector( '#changeFields' ).innerHTML = change
    }
    setDeleteConfirmMessage( recordId ) {
        const confirmMessage = `Area you sure to delete transaction with id ${ recordId } ?`
        document.getElementById( 'delete_confirm_massage_id' ).innerHTML = confirmMessage
        document.getElementById( 'delete_confirm_massage_id' ).value = recordId
    }
    clearFormFilter() {
        document.querySelector( '#productFields' ).value = ''
        document.querySelector( '#discountFields' ).value = ''
        document.querySelector( '#cashierFields' ).value = ''
        // the last fields is an input fields for adding new transaction
        document.querySelector( '#productInputFields' ).value = ''

    }
    clearAddNewDataForm() {
        document.querySelector( '#productIdFields' ).value = ''
        document.querySelector( '#discountIdFields' ).value = ''
        document.querySelector( '#startDateFields' ).value = ''
        document.querySelector( '#expiredDateFields' ).value = ''
    }
    addCashierTableRows( recordsRow ) {
        let tableCashier = $( '#product_sold_cart_datatable_id' ).DataTable()
        tableCashier.rows.add( recordsRow ).draw()
    }
    registerOnHideModal() {
        $( document ).on( 'hidden.bs.modal', '#id_modal_for_add_new_data', () => {
            new DatatableProductSoldImpl().clearCashierTable()
            new ButtonEventImpl().hideDetailCheckout()
            new ButtonEventImpl().resetDetailCheckout()
        } )
    }
}

class ButtonEventImpl extends ButtonEvent {
    constructor() {
        super()
    }
    checkOutTransaction() {
        let tableCashier = $( '#product_sold_cart_datatable_id' ).DataTable()
        let shopingItems = tableCashier.rows().data().toArray()
        if ( shopingItems.length < 1 ) {
            new Alert().showWarning( 'No product selected' )
            this.hideDetailCheckout()
            this.resetDetailCheckout()

            return
        }
        this.showDetailCheckout()
        this.setNetTotalPriceAndTax()
    }
    isExistInCashierTable( productId ) {
        let tableCashier = $( '#product_sold_cart_datatable_id' ).DataTable()
        let shopingItems = tableCashier.rows().data().toArray()
        for ( let productInCart of shopingItems ) {
            if ( productId == productInCart.product_id ) {
                return true
            }
        }
        return false
    }
    saveNewTransaction() {
        let newTransactionParams = this.serializeDataFromTableCashier()
        newTransactionParams.cashier_id = 1 // set 1 as default cashier, because cashier data came from login session.
        const validationResult = new FormValidationImpl().validateInsertParams( newTransactionParams )
        if ( !validationResult.isValid ) {
            new Alert().showWarning( validationResult.message )
            return
        }

        new ModalFormImpl().disableFormButton( '#btn_pay_transaction' )
        new AjaxImpl().saveNewTransaction( newTransactionParams )

    }
    calculateTotalPrice( productSolds ) {
        let grossTotalPrice = 0
        for ( let product of productSolds ) {
            let quantity = document.querySelector( `#input_for_quantity_${ product.product_id }` ).value
            if ( quantity < 1 ) quantity = 1;
            let grossPrice = product.price * quantity
            grossTotalPrice += grossPrice
        }
        return grossTotalPrice
    }
    calculateTotalCuttOff( productSolds ) {
        const getCuttOff = ( product ) => {
            if ( !product.discount_applied ) return 0;
            if ( !product.discount_applied.discount_applied_on_product ) return 0;
            return new FormDataImpl().getDiscountNamesForCashier( product.discount_applied.discount_applied_on_product ).discount_nominal
        }
        let cuttOffTotalPrice = 0
        for ( let product of productSolds ) {
            let quantity = document.querySelector( `#input_for_quantity_${ product.product_id }` ).value
            if ( quantity < 1 ) quantity = 1;
            let cuttOffNominal = getCuttOff( product ) * quantity
            cuttOffTotalPrice += cuttOffNominal
        }
        return cuttOffTotalPrice
    }
    calculateTax( productSolds ) {
        let netPrice = new ButtonEventImpl().calculateTotalPrice( productSolds )
        let totalCutOff = new ButtonEventImpl().calculateTotalCuttOff( productSolds )
        return ( netPrice - totalCutOff ) * 0.1
    }
    calculateChange( productSolds ) {
        let netTotalPrice = new ButtonEventImpl().calculateTotalPrice( productSolds )
        let totalCutOff = new ButtonEventImpl().calculateTotalCuttOff( productSolds )
        let tax = new ButtonEventImpl().calculateTax( productSolds )
        let paid = parseInt( document.querySelector( '#paidFields' ).value )
        return paid - ( netTotalPrice - totalCutOff + tax )
    }
    getDiscountAppliedOnProductTransaction( discountApplieds ) {
        if ( !discountApplieds ) return [];
        if ( !discountApplieds.discount_applied_on_product ) return [];

        let allDiscountApplied = []
        for ( let discount of discountApplieds.discount_applied_on_product ) {
            let discountAppliedOnProduct = {
                discount_id: discount.discount_master.discount_id,
                discount_type_id: discount.discount_master.discount_type.discount_type_id,
                cutt_off_nominal: discount.discount_master.discount_nominal
            }
            allDiscountApplied.push( discountAppliedOnProduct )
        }
        return allDiscountApplied
    }
    getItemFromSerializedData( productSoldData ) {
        const getQuantityValue = ( product ) => {
            let textQuantityValue = document.querySelector( `#input_for_quantity_${ product.product_id }` ).value
            try {
                let quantityValue = parseInt( textQuantityValue )
                return quantityValue
            }
            catch {
                return 0
            }
        }
        let allProductSolds = []
        for ( let product of productSoldData ) {
            let productDetail = {
                product_id: product.product_id,
                quantity: getQuantityValue( product ),
                product_price: product.price,
                discount_applied: this.getDiscountAppliedOnProductTransaction( product.discount_applied )
            }
            allProductSolds.push( productDetail )
        }
        return allProductSolds
    }
    serializeDataFromTableCashier() {
        let tableCashier = $( '#product_sold_cart_datatable_id' ).DataTable()
        let shopingItems = tableCashier.rows().data().toArray()
        let netTotalPrice = new ButtonEventImpl().calculateTotalPrice( shopingItems )
        let totalCuttOff = new ButtonEventImpl().calculateTotalCuttOff( shopingItems )
        let totalPriceToPaid = parseInt( netTotalPrice ) - parseInt( totalCuttOff )

        let tax = new ButtonEventImpl().calculateTax( shopingItems )
        let transactionRecord = {
            total_price: totalPriceToPaid,
            tax: tax,
            change: new ButtonEventImpl().calculateChange( shopingItems ),
            paid: parseInt( document.querySelector( '#paidFields' ).value ),
            payment_method: parseInt( document.querySelector( '#paymentMethodFields' ).value ),
            cashier_id: null,
            transaction_date: new Date().toISOString().slice( 0, 10 ),
            product_sold: new ButtonEventImpl().getItemFromSerializedData( shopingItems )
        }
        return transactionRecord
    }
    setNetTotalPriceAndTax() {
        const tableCashier = $( '#product_sold_cart_datatable_id' ).DataTable()
        const shopingItems = tableCashier.rows().data().toArray()
        let netTotalPrice = new ButtonEventImpl().calculateTotalPrice( shopingItems )
        let totalCuttOff = new ButtonEventImpl().calculateTotalCuttOff( shopingItems )
        let tax = new ButtonEventImpl().calculateTax( shopingItems )
        document.querySelector( '#netPriceFields' ).innerHTML = netTotalPrice
        document.querySelector( '#taxFields' ).innerHTML = tax
        document.querySelector( '#cuttOffFields' ).innerHTML = totalCuttOff
        document.querySelector( '#priceToPayFields' ).innerHTML = tax + ( netTotalPrice - totalCuttOff )
    }
    resetDetailCheckout() {
        document.querySelector( '#netPriceFields' ).textContent = 0;
        document.querySelector( '#taxFields' ).textContent = 0;
        document.querySelector( '#cuttOffFields' ).textContent = 0;
        document.querySelector( '#changeFields' ).innerHTML = 0
        document.querySelector( '#paidFields' ).value = 0
    }
    showDetailCheckout() {
        document.querySelector( '#container_detail_checkout' ).removeAttribute( 'hidden' )
    }
    hideDetailCheckout() {
        document.querySelector( '#container_detail_checkout' ).hidden = true
    }
    bindEventWithAjax() {
        const buttonDelete = document.querySelector( this.btnDeleteId )
        buttonDelete.addEventListener( 'click', this.deleteData )
    }
    saveNewData() {
        const insertParams = new FormDataImpl().getAddNewDataFormValues()
        const validationResult = new FormValidationImpl().validateInsertParams( insertParams )
        if ( !validationResult.isValid ) {
            new Alert().showWarning( validationResult.message )
            new ModalFormImpl().enableFormButton( new ButtonSelector().saveNewRecord )
            return
        }
        new ModalFormImpl().disableFormButton( new ButtonSelector().saveNewRecord )
        new AjaxImpl().saveNewRecord( insertParams )
    }

    deleteData() {
        const deleteParams = new FormDataImpl().getDeleteFormValues()
        const validationResult = new FormValidationImpl().validateDeleteParams( deleteParams )
        if ( !validationResult.isValid ) {
            new Alert().showWarning( validationResult.message )
            new ModalFormImpl().enableFormButton( new ButtonSelector().btnDeleteId )
            return
        }
        new ModalFormImpl().disableFormButton( new ButtonSelector().btnDeleteId )
        new AjaxImpl().deleteData( deleteParams )
    }
}
class AjaxImpl extends Ajax {
    constructor() {
        super()
    }
    saveNewTransaction( formData ) {
        const payload = this.createPayload( 'POST', formData )
        const onSuccess = ( response ) => {
            if ( response.status ) {
                new Alert().successAjax( response.msg )
                new DatatableProductSoldImpl().reloadDatatable()
                new DatatableProductSoldImpl().clearCashierTable()
                new ButtonEventImpl().hideDetailCheckout()
                new ButtonEventImpl().resetDetailCheckout()
                return
            }
            new Alert().failedAjax( response.msg )
        }
        const ajaxCallback = {
            onSuccess: onSuccess,
            onFail: ( error ) => {
                new Alert().error()
            },
            onFinal: () => {
                new ModalForm().enableFormButton( '#btn_pay_transaction' )
            }
        }
        this.sendAjax( { url: '/product_sold_api', payload: payload }, ajaxCallback )
    }
    getSingleData( recordId ) {
        const params = {
            transaction_id: recordId
        }
        const payload = this.createPayload( 'POST', params )
        const onSuccess = ( response ) => {
            if ( !response.data.length ) new Alert().failedAjax( response.msg );
            new FormDataImpl().setDetailModalTables( response.data[ 0 ].detail_transaction )
            return
        }
        const ajaxCallback = {
            onSuccess: onSuccess,
            onFail: ( error ) => {
                new Alert().error()
            },
            onFinal: () => { }
        }
        this.sendAjax( { url: '/product_sold_api_search', payload: payload }, ajaxCallback )
    }

    getSingleProduct( recordId ) {
        const params = {
            product_id: recordId
        }
        const payload = this.createPayload( 'POST', params )
        const onSuccess = ( response ) => {
            if ( !response.data.length ) return new Alert().failedAjax( response.msg );
            new FormDataImpl().addItemToCashierTable( response.data[ 0 ] )
            return
        }
        const ajaxCallback = {
            onSuccess: onSuccess,
            onFail: ( error ) => {
                new Alert().error()
            },
            onFinal: () => { }
        }
        this.sendAjax( { url: '/product_api_search', payload: payload }, ajaxCallback )
    }
    deleteData( formData ) {
        const payload = this.createPayload( 'DELETE', formData )
        const onSuccess = ( response ) => {
            if ( !response.status ) {
                return new Alert().failedAjax( response.msg )
            }
            new Alert().successAjax( response.msg )
            new DatatableProductSoldImpl().reloadDatatable()
            new ModalFormImpl().hideModal( 'id_modal_for_delete' )
            return
        }
        const ajaxCallback = {
            onSuccess: onSuccess,
            onFail: ( error ) => {
                new Alert().error()
            },
            onFinal: () => {
                new ModalFormImpl().enableFormButton( '#button_delete_data_id' )
            }
        }

        this.sendAjax( { url: '/product_sold_api', payload: payload }, ajaxCallback )
    }
    getOption( endPoint, onSuccess = () => { } ) {
        return fetch( endPoint )
            .then( response => response.json() )
            .then( onSuccess )
            .catch( ( err ) => { console.log( err ) } ).finally( () => {
                return Promise.resolve( 1 )
            } )
    }
    getLovForProductFields() {
        const extractIdDescriptionFunc = ( recordValues ) => {
            let newRecordValues = []
            for ( const record of recordValues ) {
                newRecordValues.push( { id: record.product_id, description: record.product_desc } )
            }
            return newRecordValues
        }
        const onSuccess = ( response ) => {
            let newRecordValues = extractIdDescriptionFunc( response.data )
            const selectFieldIds = [ '#productFields', '#productInputFields' ]
            new FormDataImpl().setOptionForSelectFields( selectFieldIds, newRecordValues )
        }
        return this.getOption( '/product_lov_api', onSuccess )
    }
    getLovForDiscountFields() {
        const extractIdDescriptionFunc = ( recordValues ) => {
            let newRecordValues = []
            for ( const record of recordValues ) {
                newRecordValues.push( { id: record.discount_id, description: record.desc } )
            }
            return newRecordValues
        }
        const onSuccess = ( response ) => {
            let newRecordValues = extractIdDescriptionFunc( response.data )
            const selectFieldIds = [ '#discountFields' ]
            new FormDataImpl().setOptionForSelectFields( selectFieldIds, newRecordValues )
        }
        return this.getOption( '/discount_lov_api', onSuccess )
    }
    getLovForEmployeeFields() {
        const extractIdDescriptionFunc = ( recordValues ) => {
            let newRecordValues = []
            for ( const record of recordValues ) {
                newRecordValues.push( { id: record.employee_id, description: record.name } )
            }
            return newRecordValues
        }
        const onSuccess = ( response ) => {
            let newRecordValues = extractIdDescriptionFunc( response.data )
            const selectFieldIds = [ '#cashierFields' ]
            new FormDataImpl().setOptionForSelectFields( selectFieldIds, newRecordValues )
        }
        return this.getOption( '/employee_lov_api', onSuccess )
    }
    getLovForPaymentMethodFields() {
        const extractIdDescriptionFunc = ( recordValues ) => {
            let newRecordValues = []
            for ( const record of recordValues ) {
                newRecordValues.push( { id: record.payment_method_id, description: record.payment_method } )
            }
            return newRecordValues
        }
        const onSuccess = ( response ) => {
            let newRecordValues = extractIdDescriptionFunc( response.data )
            const selectFieldIds = [ '#paymentMethodFields' ]
            new FormDataImpl().setOptionForSelectFields( selectFieldIds, newRecordValues )
        }
        return this.getOption( '/payment_method_lov_api', onSuccess )
    }
    getLovForSelectField() {
        const callLovAjax = async () => {
            const promiseList = [ this.getLovForProductFields(), this.getLovForDiscountFields(), this.getLovForEmployeeFields(), this.getLovForPaymentMethodFields() ]
            await Promise.all( promiseList ).then( () => {
                new ModalFormImpl().clearFormFilter()
                new ModalFormImpl().createSelectFields()
            } )
        }
        callLovAjax()
    }
}

const runScript = () => {
    $( document ).ready( function () {
        const modalForm = new ModalFormImpl()
        const datatable = new DatatableProductSoldImpl()
        new AjaxImpl().getLovForSelectField()
        new ButtonEventImpl().bindEventWithAjax()
        datatable.initiateDatatable()
        datatable.initiateDatatableForTransactionChart()
        modalForm.bindEventToFormFilterAndNewTransaction()
        modalForm.registerOnHideModal()
    } )
}

runScript()
