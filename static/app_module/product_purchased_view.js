const runScript = () => {
    $( document ).ready( function () {
        const modalForm = new ModalFormImpl()
        const datatable = new DatatableProductPurchasedImpl()
        const btnEvent = new ButtonEventImpl()
        new AjaxImpl().getLovForSelectField()
        btnEvent.bindEventWithAjax()
        btnEvent.setAsActiveMenu()
        datatable.initiateDatatable()
        datatable.initiateDatatableForTransactionChart()
        modalForm.bindEventToFormFilterAndNewTransaction()
        modalForm.registerOnHideModal()
    } )
}

runScript()


class DatatableProductPurchasedImpl extends BaseDatatable {
    constructor() {
        super()
        this.tableColumns = [
            {
                data: null,
                defaultContent: ''
            },
            {
                data: 'purchased_transaction_id'
            },
            {
                data: 'purchasing_date'
            },
            {
                data: 'payment_method',
                render: ( data ) => {
                    return data.payment_method
                }
            },
            {
                data: 'nominal'
            },
            {
                data: 'supplier',
                render: ( data ) => {
                    return data.supplier
                }
            },

            {
                data: null,
                render: ( data ) => {
                    const buttonDetail = `<button type="button" class="btn btn-warning btn-detail-data" value=${ data.purchased_transaction_id } onclick="new ModalForm().showModal('id_modal_for_detail_data')">Detail</button>`
                    return buttonDetail + '&nbsp;' + this.buttonDelete.replace( "_data_", data.purchased_transaction_id )
                }
            }
        ]
        this.columnName = [
            { "name": "no", "targets": 0 },
            { "name": "transaction_purchased_id", "targets": 1 },
            { "name": "purchasing_date", "targets": 2 },
            { "name": "payment_method", "targets": 3 },
            { "name": "nominal", "targets": 4 },
            { "name": "supplier", "targets": 5 },
            { "name": "action", "targets": 6 }
        ]
        this.datatableId = '#product_purchased_transaction_datatable_id'
        this.apiEndpoint = '/product_purchased_api'
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
                    data.supplier_id = getDataFromFields( '#supplierFields' )
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
    initiateDatatableForTransactionChart() {
        const tableCashierSettings = {
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
                    data: 'btnRemove',
                    default: ''
                }
            ]
        }
        const tableCashier = $( '#product_purchased_cart_datatable_id' ).DataTable( tableCashierSettings )
        tableCashier.on( 'draw.dt order.dt search.dt', function () {
            tableCashier.column( 0, { search: 'applied', order: 'applied' } ).nodes().each( function ( cell, i ) {
                cell.innerHTML = i + 1;
            } );
        } ).draw();
        $( '#product_purchased_cart_datatable_id' ).on( 'click', '.btn-remove-data', function () {
            const table = $( '#product_purchased_cart_datatable_id' ).DataTable()
            table.row( $( this ).parents( 'tr' ) ).remove().draw();
            new ButtonEventImpl().hideDetailCheckout()
            new ButtonEventImpl().resetDetailCheckout()
        } )
        $( '#product_purchased_cart_datatable_id' ).on( 'input', '.quantityFields', function ( event ) {
            if ( !this.value ) return;
            let newQuantity = parseInt( this.value )
            if ( newQuantity < 1 ) newQuantity = 1;

            const table = $( '#product_purchased_cart_datatable_id' ).DataTable()
            let currentRowData = table.row( $( this ).parents( 'tr' ) ).data()
            let newRowData = { ...currentRowData }

            newRowData.sub_total = currentRowData.price * newQuantity
            newRowData.quantity = new FormDataImpl().getQuantityTemplate( newRowData, newQuantity )
            console.log( newRowData )
            table.row( $( this ).parents( 'tr' ) ).data( newRowData ).invalidate().draw()
        } )
    }
    bindEventForActionsButton( datatableInstance ) {
        datatableInstance.on( 'click', '.btn-detail-data', function ( e ) {
            new AjaxImpl().getSingleData( e.target.value )
        } )
        datatableInstance.on( 'click', this.btnClassDeleteData, ( e ) => {
            new ModalFormImpl().setDeleteConfirmMessage( e.target.value )
        } )
    }
    clearCashierTable() {
        let table = $( '#product_purchased_cart_datatable_id' ).DataTable();
        table.clear().draw();
    }
}

class ButtonEventImpl extends ButtonEvent {
    constructor() {
        super()
    }
    setAsActiveMenu() {
        document.querySelector( '#purchased_product_side_link' ).classList.add( 'active' )
    }
    bindEventWithAjax() {
        const buttonDelete = document.querySelector( this.btnDeleteId )
        buttonDelete.addEventListener( 'click', this.deleteData )
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
    saveNewTransaction() {
        let newTransactionParams = this.serializeDataFromTableCashier()
        const validationResult = new FormValidationImpl().validateInsertParams( newTransactionParams )
        if ( !validationResult.isValid ) {
            new Alert().showWarning( validationResult.message )
            return
        }
        new ModalFormImpl().disableFormButton( '#btn_pay_transaction' )
        new AjaxImpl().saveNewTransaction( newTransactionParams )

    }

    checkOutTransaction() {
        let tableCashier = $( '#product_purchased_cart_datatable_id' ).DataTable()
        let shopingItems = tableCashier.rows().data().toArray()
        if ( shopingItems.length < 1 ) {
            new Alert().showWarning( 'No product selected' )
            this.hideDetailCheckout()
            this.resetDetailCheckout()

            return
        }
        this.showDetailCheckout()
        this.setNetTotalPrice()
    }

    showDetailCheckout() {
        document.querySelector( '#container_detail_checkout' ).removeAttribute( 'hidden' )
    }
    hideDetailCheckout() {
        document.querySelector( '#container_detail_checkout' ).hidden = true
    }

    serializeDataFromTableCashier() {
        let tableCashier = $( '#product_purchased_cart_datatable_id' ).DataTable()
        let shopingItems = tableCashier.rows().data().toArray()
        let netTotalPrice = new ButtonEventImpl().calculateTotalPrice( shopingItems )
        let transactionRecord = {
            nominal: netTotalPrice,
            supplier_id: parseInt( document.querySelector( '#supplierInputFields' ).value ),
            payment_method: parseInt( document.querySelector( '#paymentMethodFields' ).value ),
            transaction_date: new Date().toISOString().slice( 0, 10 ),
            product_purchased: new ButtonEventImpl().getItemFromSerializedData( shopingItems )
        }
        return transactionRecord
    }

    getItemFromSerializedData( productPurchasedData ) {
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
        let allProductPurchaseds = []
        for ( let product of productPurchasedData ) {
            let productDetail = {
                product_id: product.product_id,
                quantity: getQuantityValue( product ),
                product_price: product.price
            }
            allProductPurchaseds.push( productDetail )
        }
        return allProductPurchaseds
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

    setNetTotalPrice() {
        const tableCashier = $( '#product_purchased_cart_datatable_id' ).DataTable()
        const shopingItems = tableCashier.rows().data().toArray()
        let netTotalPrice = new ButtonEventImpl().calculateTotalPrice( shopingItems )
        document.querySelector( '#netPriceFields' ).innerHTML = netTotalPrice
    }
    resetDetailCheckout() {
        document.querySelector( '#netPriceFields' ).textContent = 0;
    }
    isExistInCashierTable( productId ) {
        let tableCashier = $( '#product_purchased_cart_datatable_id' ).DataTable()
        let shopingItems = tableCashier.rows().data().toArray()
        for ( let productInCart of shopingItems ) {
            if ( productId == productInCart.product_id ) {
                return true
            }
        }
        return false
    }
    calculateTotalPrice( ProductPurchaseds ) {
        let grossTotalPrice = 0
        for ( let product of ProductPurchaseds ) {
            let quantity = document.querySelector( `#input_for_quantity_${ product.product_id }` ).value
            if ( quantity < 1 ) quantity = 1;
            let grossPrice = product.price * quantity
            grossTotalPrice += grossPrice
        }
        return grossTotalPrice
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
                new DatatableProductPurchasedImpl().reloadDatatable()
                new DatatableProductPurchasedImpl().clearCashierTable()
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
        this.sendAjax( { url: '/product_purchased_api', payload: payload }, ajaxCallback )
    }
    getSingleData( recordId ) {
        const params = {
            transaction_purchased_id: recordId
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
        this.sendAjax( { url: '/product_purchased_api_search', payload: payload }, ajaxCallback )
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
            new DatatableProductPurchasedImpl().reloadDatatable()
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

        this.sendAjax( { url: '/product_purchased_api', payload: payload }, ajaxCallback )
    }
    getLovForSelectField() {
        const callLovAjax = async () => {
            const promiseList = [ this.getLovForProductFields(), this.getLovForSupplierFields(), this.getLovForPaymentMethodFields() ]
            await Promise.all( promiseList ).then( () => {
                new ModalFormImpl().clearFormFilter()
                new ModalFormImpl().createSelectFields()
            } )
        }
        callLovAjax()
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
    getLovForSupplierFields() {
        const extractIdDescriptionFunc = ( recordValues ) => {
            let newRecordValues = []
            for ( const record of recordValues ) {
                newRecordValues.push( { id: record.supplier_id, description: record.supplier } )
            }
            return newRecordValues
        }
        const onSuccess = ( response ) => {
            let newRecordValues = extractIdDescriptionFunc( response.data )
            const selectFieldIds = [ '#supplierFields', '#supplierInputFields' ]
            new FormDataImpl().setOptionForSelectFields( selectFieldIds, newRecordValues )
        }
        return this.getOption( '/supplier_lov_api', onSuccess )
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
    getOption( endPoint, onSuccess = () => { } ) {
        return fetch( endPoint )
            .then( response => response.json() )
            .then( onSuccess )
            .catch( ( err ) => { console.log( err ) } ).finally( () => {
                return Promise.resolve( 1 )
            } )
    }
}

class FormDataImpl extends FormData {
    constructor() {
        super()
    }
    getDeleteFormValues() {
        let formValues = {
            transaction_purchased_id: document.getElementById( 'delete_confirm_massage_id' ).value
        }
        return formValues
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
            productRecord: productRecord,
            btnRemove: removeRecordBtn
        }
        new ModalFormImpl().addCashierTableRows( [ records ] )
    }
    setDetailModalTables( recordValues ) {
        let tableContent = ""
        for ( let [ index, record ] of recordValues.entries() ) {
            record.index = index
            record.sub_total = record.purchased_price * record.quantity
            tableContent += this.generateRow( record )
        }
        let table = document.querySelector( '#product_purchased_detail_transaction_datatable_id > tbody' )
        table.innerHTML = tableContent
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
                            <td>${ replaceEmpty( record.purchased_price ) }</td>
                            <td>${ replaceEmpty( record.sub_total ) }</td>
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
    validateDeleteParams( deleteParams ) {
        const validTransactionId = this.validateTransactionId( deleteParams )
        if ( !validTransactionId.isValid ) return validTransactionId;
        return this.validateResult( 'Data is valid', true )
    }
    validateInsertParams( insertParams ) {

        const validPaymentMethodId = this.validatePaymentMethodId( insertParams )
        const validSupplierID = this.validateSupplierID( insertParams )
        const validProductPurchased = this.validateProductPurchased( insertParams.product_purchased )

        if ( !validProductPurchased.isValid ) return validProductPurchased;
        if ( !validSupplierID.isValid ) return validSupplierID;
        if ( !validPaymentMethodId.isValid ) return validSupplierID;

        return this.validateResult( 'Data is valid', true )
    }
    validateProductPurchased( productPurchasedData ) {
        if ( !productPurchasedData.length ) {
            return this.validateResult( 'No product selected' )
        }

        for ( let product of productPurchasedData ) {
            if ( !product.product_id ) {
                return this.validateResult( 'Invalid product selected' )
            }
            if ( !product.product_price ) {
                return this.validateResult( 'There is invalid value for product selected' )
            }
            if ( product.quantity < 1 ) {
                return this.validateResult( 'Product quantity cant less than 1' )
            }
        }
        return this.validateResult( 'Data is valid', true )
    }
    validateSupplierID( formData ) {
        if ( !formData.supplier_id ) {
            return this.validateResult( 'Supplier is not selected' )
        }
        if ( isNaN( formData.supplier_id ) ) {
            return this.validateResult( 'Supplier is not valid' )
        }
        return this.validateResult( 'Data is valid', true )
    }
    validatePaymentMethodId( formData ) {
        if ( !formData.payment_method ) {
            return this.validateResult( 'Payment method is not' )
        }
        if ( isNaN( formData.payment_method ) ) {
            return this.validateResult( 'Payment method is not valid' )
        }
        return this.validateResult( 'Data is valid', true )
    }
    validateTransactionId( formData ) {
        if ( isNaN( formData.transaction_purchased_id ) ) {
            return this.validateResult( 'Invalid transaction selected' )
        }
        if ( !( parseInt( formData.transaction_purchased_id ) ) ) {
            return this.validateResult( 'Invalid transaction selected' )
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

    registerOnHideModal() {
        $( document ).on( 'hidden.bs.modal', '#id_modal_for_add_new_data', () => {
            new DatatableProductPurchasedImpl().clearCashierTable()
            new ButtonEventImpl().hideDetailCheckout()
            new ButtonEventImpl().resetDetailCheckout()
        } )
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

                const isExist = new ButtonEventImpl().isExistInCashierTable( productId )
                if ( isExist ) {
                    new ModalFormImpl().increaseProductQuantity( productId )
                    return
                }
                new AjaxImpl().getSingleProduct( productId )
            }
        } );
    }
    bindEventToFormFilterAndNewTransaction() {
        const btnFilterData = document.querySelector( '.btn-filter-product-purchased' )
        const btnCheckout = document.querySelector( '.btn-checkout-product-purchased' )

        btnFilterData.addEventListener( 'click', () => {
            new DatatableProductPurchasedImpl().reloadDatatable()
        } )
        btnCheckout.addEventListener( 'click', () => {
            new ButtonEventImpl().checkOutTransaction()
        } )

        const payTransaction = document.querySelector( '.btn-pay-product-purchased' )
        payTransaction.addEventListener( 'click', () => {
            new ButtonEventImpl().saveNewTransaction()
        } )

    }
    setDeleteConfirmMessage( recordId ) {
        const confirmMessage = `Area you sure to delete transaction with id ${ recordId } ?`
        document.getElementById( 'delete_confirm_massage_id' ).innerHTML = confirmMessage
        document.getElementById( 'delete_confirm_massage_id' ).value = recordId
    }
    increaseProductQuantity( productId ) {
        let quantityField = document.querySelector( `#input_for_quantity_${ productId }` )
        let oldQuantity = quantityField.value
        quantityField.value = parseInt( oldQuantity ) + 1
        $( `#input_for_quantity_${ productId }.quantityFields` ).trigger( 'input' )
    }

    addCashierTableRows( recordsRow ) {
        let tableCashier = $( '#product_purchased_cart_datatable_id' ).DataTable()
        tableCashier.rows.add( recordsRow ).draw()
    }
    clearFormFilter() {
        document.querySelector( '#productFields' ).value = ''
        document.querySelector( '#supplierFields' ).value = ''
        document.querySelector( '#productInputFields' ).value = ''
    }

}


