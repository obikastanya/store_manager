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
            { "name": "product_code", "targets": 1 },
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
            warehouse_stock: get( '#warehouseStockFields' ),
            store_stock: get( '#storeStockFields' ),
            product_id: get( '#idProductFields' )
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
        set( '#idStockHiddenFields' ).value = recordValues.stock_id
        set( '#warehouseStockUpdateFields' ).value = recordValues.warehouse_stock
        set( '#storeStockUpdateFields' ).value = recordValues.store_stock
        set( '#idProductUpdateFields' ).value = recordValues.product_id
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
        const validIdCompany = this.validateIdCompany( updateParams )
        const validCompany = this.validateCompany( updateParams )
        const validActiveStatus = this.validateActiveStatus( updateParams )

        if ( !validIdCompany.isValid ) return validIdCompany;
        if ( !validCompany.isValid ) return validCompany;
        if ( !validActiveStatus.isValid ) return validActiveStatus;
        return this.validateResult( 'Data is valid', true )
    }
    validateDeleteParams( deleteParams ) {
        if ( !deleteParams.company_id || deleteParams.company_id.length < 0 ) {
            return this.validateResult( 'Company Id doesnt found' )
        }
        return this.validateResult( 'Data is valid', true )
    }
    validateInsertParams( insertParams ) {
        return this.validateCompany( insertParams )
    }
    validateCompany( formData ) {
        if ( !formData.company ) {
            return this.validateResult( 'Cant insert empty data' )
        }
        if ( formData.company.length < 3 ) {
            return this.validateResult( 'Company Name too short' )
        }
        if ( formData.company.length > 200 ) {
            return this.validateResult( 'Company Name too long' )
        }
        return this.validateResult( 'Data is valid', true )
    }
    validateIdCompany( formData ) {
        if ( !formData.company_id || formData.company_id.length < 0 ) {
            return this.validateResult( 'There is no company id to update' )
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
    setDeleteConfirmMessage( formValues ) {
        const confirmMessage = `Area you sure to delete ${ formValues.company_id } - ${ formValues.company } ?`
        document.getElementById( 'delete_confirm_massage_id' ).innerHTML = confirmMessage
        document.getElementById( 'delete_confirm_massage_id' ).value = formValues.company_id
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
        const payload = this.createPayload( 'POST', { 'company_id': recordId } )
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
        const payload = this.createPayload( 'POST', { 'company_id': recordId } )
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

const runScript = () => {
    $( document ).ready( function () {
        const modalForm = new ModalFormImpl()
        new DatatableStockImpl().initiateDatatable()
        new AjaxImpl().getOptionForProductMaster()
        modalForm.registerOnHideModal()
        modalForm.disabledBtnNewDataOnClick()
        new ButtonEventImpl().bindEventWithAjax()
    } )
}

runScript()
