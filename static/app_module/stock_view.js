const runScript = () => {
    $( document ).ready( function () {
        const modalForm = new ModalFormImpl()
        new DatatableStockImpl().initiateDatatable()
        new AjaxImpl().getOptionForProductMaster()
        modalForm.registerOnHideModal()
        modalForm.disabledBtnNewDataOnClick()

        const btnEvent = new ButtonEventImpl()
        btnEvent.bindEventWithAjax()
        btnEvent.setMasterAsActiveMenu()

    } )
}

runScript()

class DatatableStockImpl extends BaseDatatable {
    constructor() {
        super()
        this.tableColumns = [
            {
                data: null,
                defaultContent: ''
            },
            {
                data: 'product',
                render: ( data ) => {
                    if ( !data ) return '-';
                    return data.product_id
                }
            },
            {
                data: 'product',
                render: ( data ) => {
                    if ( !data ) return '-';
                    return data.product_desc
                }
            },
            { data: 'warehouse_stock' },
            { data: 'store_stock' },
            {
                data: null,
                render: ( data ) => {
                    return this.buttonEdit.replace( "_data_", data.stock_id ) + '&nbsp;' + this.buttonDelete.replace( "_data_", data.stock_id )
                }
            }
        ]
        this.columnName = [
            { "name": "no", "targets": 0 },
            { "name": "product_id", "targets": 1 },
            { "name": "product_desc", "targets": 2 },
            { "name": "warehouse_stock", "targets": 3 },
            { "name": "store_stock", "targets": 4 },
            { "name": "action", "targets": 5 }
        ]
        this.datatableId = '#stock_datatable_id'
        this.apiEndpoint = '/stock_api'
    }
    bindEventForActionsButton( datatableInstance ) {
        datatableInstance.on( 'click', this.btnClassEditData, function ( e ) {
            new AjaxImpl().getSingleData( e.target.value )
        } )
        datatableInstance.on( 'click', this.btnClassDeleteData, ( e ) => {
            new AjaxImpl().getSingleDataForDeleteActions( e.target.value )
        } )
    }
}


class ButtonEventImpl extends ButtonEvent {
    constructor() {
        super()
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
    saveUpdatedData() {
        const updateParams = new FormDataImpl().getUpdateFormValues()
        console.log( updateParams )
        const validationResult = new FormValidationImpl().validateUpdateParams( updateParams )
        if ( !validationResult.isValid ) {
            new Alert().showWarning( validationResult.message )
            new ModalFormImpl().enableFormButton( new ButtonSelector().btnSaveUpdatedRecord )
            return
        }
        new ModalFormImpl().disableFormButton( new ButtonSelector().btnSaveUpdatedRecord )
        new AjaxImpl().updateData( updateParams )
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
    saveNewRecord( formData ) {
        const payload = this.createPayload( 'POST', formData )
        const onSuccess = ( response ) => {
            if ( response.status ) {
                new ModalFormImpl().hideModal( 'id_modal_for_add_new_data' )
                new Alert().successAjax( response.msg )
                new DatatableStockImpl().reloadDatatable()
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
                new ModalForm().enableSaveConfirmBtn()
            }
        }
        this.sendAjax( { url: '/stock_api', payload: payload }, ajaxCallback )
    }
    getSingleData( recordId ) {
        const payload = this.createPayload( 'POST', { 'stock_id': recordId } )
        const onSuccess = ( response ) => {
            console.log( response )
            if ( !response.data.length ) new Alert().failedAjax( response.msg );
            let recordValues = response.data[ 0 ]

            // the script bellow is a tenary operator, its update active_status to 1 if the current value is Y and 0 for others.
            recordValues.active_status = recordValues.active_status == 'Y' ? 1 : 0

            new FormDataImpl().setUpdateFormValues( recordValues )
            return
        }
        const ajaxCallback = {
            onSuccess: onSuccess,
            onFail: ( error ) => {
                new Alert().error()
            },
            onFinal: () => { }
        }
        this.sendAjax( { url: '/stock_api_search', payload: payload }, ajaxCallback )
    }
    getSingleDataForDeleteActions( recordId ) {
        const payload = this.createPayload( 'POST', { 'stock_id': recordId } )
        const onSuccess = ( response ) => {
            if ( !response.data.length ) new Alert().failedAjax( response.msg );
            let recordValues = response.data[ 0 ]
            // the script bellow is a tenary operator, its update active_status to 1 if the current value is Y and 0 for others.
            recordValues.active_status = recordValues.active_status == 'Y' ? 1 : 0
            new ModalFormImpl().setDeleteConfirmMessage( recordValues )
            return
        }
        const ajaxCallback = {
            onSuccess: onSuccess,
            onFail: ( error ) => {
                new Alert().error()
            },
            onFinal: () => { }
        }
        this.sendAjax( { url: '/stock_api_search', payload: payload }, ajaxCallback )

    }
    updateData( formData ) {
        const payload = this.createPayload( 'PUT', formData )
        const onSuccess = ( response ) => {
            if ( !response.status ) {
                return new Alert().failedAjax( response.msg )
            }
            new Alert().successAjax( response.msg )
            new DatatableStockImpl().reloadDatatable()
            new ModalFormImpl().hideModal( 'id_modal_for_edit' )
            return
        }
        const ajaxCallback = {
            onSuccess: onSuccess,
            onFail: ( error ) => {
                new Alert().error()
            },
            onFinal: () => {
                new ModalFormImpl().enableFormButton( '#button_save_updated_data_id' )
            }
        }
        this.sendAjax( { url: '/stock_api', payload: payload }, ajaxCallback )

    }
    deleteData( formData ) {
        const payload = this.createPayload( 'DELETE', formData )
        const onSuccess = ( response ) => {
            if ( !response.status ) {
                return new Alert().failedAjax( response.msg )
            }
            new Alert().successAjax( response.msg )
            new DatatableStockImpl().reloadDatatable()
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
        this.sendAjax( { url: '/stock_api', payload: payload }, ajaxCallback )
    }
    getOptionForProductMaster() {
        const onSuccess = ( response ) => {
            new FormDataImpl().setOptionForProductMaster( response.data )
        }
        const ajaxCallback = {
            onSuccess: onSuccess,
            onFail: ( err ) => { console.log( err ) }
        }
        fetch( '/product_api' )
            .then( response => response.json() )
            .then( onSuccess )
            .catch( ajaxCallback.onFail )
    }
}


class FormDataImpl extends FormData {
    constructor() {
        super()
    }
    getAddNewDataFormValues() {
        const get = ( idElement ) => {
            return document.querySelector( idElement ).value
        }
        let formValues = {
            warehouse_stock: get( '#warehouseStockFields' ),
            store_stock: get( '#storeStockFields' ),
            product_id: get( '#idProductFields' )
        }
        return formValues
    }
    getDeleteFormValues() {
        let formValues = {
            stock_id: document.getElementById( 'delete_confirm_massage_id' ).value
        }
        return formValues
    }
    getUpdateFormValues() {
        const get = ( idElement ) => {
            return document.querySelector( idElement ).value
        }
        let formValues = {
            stock_id: get( '#idStockHiddenFields' ),
            warehouse_stock: get( '#warehouseStockUpdateFields' ),
            store_stock: get( '#storeStockUpdateFields' ),
            product_id: get( '#idProductUpdateFields' )
        }
        return formValues
    }
    generateOption( recordValues ) {
        let options = ''
        for ( const values of recordValues ) {
            options += ` <option value=${ values.product_id }>${ values.product_desc }</option> `
        }
        return options
    }
    setUpdateFormValues( recordValues ) {
        const set = ( idElement ) => {
            return document.querySelector( idElement )
        }
        const setIfExistProductId = ( value ) => {
            if ( !value ) return '';
            return value.product_id
        }
        const setIfExistProductDesc = ( value ) => {
            if ( !value ) return '';
            return value.product_desc
        }
        set( '#idStockHiddenFields' ).value = recordValues.stock_id
        set( '#warehouseStockUpdateFields' ).value = recordValues.warehouse_stock
        set( '#storeStockUpdateFields' ).value = recordValues.store_stock
        set( '#idProductUpdateFields' ).value = setIfExistProductId( recordValues.product )
        set( '#productDescUpdateFields' ).value = setIfExistProductDesc( recordValues.product )
    }
    setOptionForProductMaster( recordValues ) {
        // some dom manipulation
        const options = this.generateOption( recordValues )
        document.querySelector( '#idProductFields' ).innerHTML = ''
        document.querySelector( '#idProductFields' ).innerHTML = options
    }
}
class FormValidationImpl extends FormValidation {
    constructor() {
        super()
    }
    validateUpdateParams( updateParams ) {
        const validIdProduct = this.validateIdProduct( updateParams )
        const validWarehouseStock = this.validateWarehouseStock( updateParams )
        const validStoreStock = this.validateStoreStock( updateParams )
        const validIdStock = this.validateIdStock( updateParams )

        if ( !validIdProduct.isValid ) return validIdProduct;
        if ( !validWarehouseStock.isValid ) return validWarehouseStock;
        if ( !validStoreStock.isValid ) return validStoreStock;
        if ( !validIdStock.isValid ) return validIdStock;
        return this.validateResult( 'Data is valid', true )
    }
    validateDeleteParams( deleteParams ) {
        if ( !deleteParams.stock_id || deleteParams.stock_id.length < 0 ) {
            return this.validateResult( 'Stock Product doesnt found' )
        }
        return this.validateResult( 'Data is valid', true )
    }
    validateInsertParams( insertParams ) {
        const validIdProduct = this.validateIdProduct( insertParams )
        const validWarehouseStock = this.validateWarehouseStock( insertParams )
        const validStoreStock = this.validateStoreStock( insertParams )

        if ( !validIdProduct.isValid ) return validIdProduct;
        if ( !validWarehouseStock.isValid ) return validWarehouseStock;
        if ( !validStoreStock.isValid ) return validStoreStock;
        return this.validateResult( 'Data is valid', true )
    }
    validateIdProduct( formData ) {
        if ( !formData.product_id ) {
            return this.validateResult( 'Product selected is not valid' )
        }
        if ( isNaN( formData.product_id ) ) {
            return this.validateResult( 'Product Id is not valid' )
        }
        return this.validateResult( 'Data is valid', true )
    }
    validateWarehouseStock( formData ) {
        if ( !formData.warehouse_stock ) {
            return this.validateResult( 'Warehouse stock is empty' )
        }
        if ( isNaN( formData.warehouse_stock ) ) {
            return this.validateResult( 'Warehouse stock must be a number' )
        }
        if ( formData.warehouse_stock < 0 ) {
            return this.validateResult( 'Warehouse stock must be zero or greater' )
        }
        return this.validateResult( 'Data is valid', true )
    }
    validateStoreStock( formData ) {
        if ( !formData.store_stock ) {
            return this.validateResult( 'Store stock is empty' )
        }
        if ( isNaN( formData.store_stock ) ) {
            return this.validateResult( 'Store stock must be a number' )
        }
        if ( formData.store_stock < 0 ) {
            return this.validateResult( 'Store stock must be zero or greater' )
        }
        return this.validateResult( 'Data is valid', true )
    }
    validateIdStock( formData ) {
        if ( !formData.stock_id ) {
            return this.validateResult( 'Stock is not valid' )
        }
        if ( isNaN( formData.stock_id ) ) {
            return this.validateResult( 'Stock is not valid' )
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
    setDeleteConfirmMessage( formValues ) {
        const confirmMessage = `Area you sure to delete ${ formValues.product.product_id } - ${ formValues.product.product_desc } ?`
        document.getElementById( 'delete_confirm_massage_id' ).innerHTML = confirmMessage
        document.getElementById( 'delete_confirm_massage_id' ).value = formValues.stock_id
    }
    clearAddNewDataForm() {
        const get = ( idElement ) => {
            return document.querySelector( idElement )
        }
        get( '#warehouseStockFields' ).value = ''
        get( '#storeStockFields' ).value = ''
        get( '#idProductFields' ).value = ''
    }
}
