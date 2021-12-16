class DatatableProductImpl extends BaseDatatable {
    constructor() {
        super()
        this.tableColumns = [
            {
                data: null,
                defaultContent: ''
            },
            { data: 'product_id' },
            { data: 'product_desc' },
            { data: 'brand' },
            { data: 'category' },
            { data: 'price' },
            { data: 'supplier' },
            { data: 'company' },
            {
                data: 'active_status',
                render: ( data ) => {
                    if ( data == 'Y' ) return 'Active';
                    return 'Non-Active'
                }
            },
            {
                data: null,
                render: ( data ) => {
                    return this.buttonEdit.replace( "_data_", data.product_id ) + '&nbsp;' + this.buttonDelete.replace( "_data_", data.product_id )
                }
            }
        ]
        this.columnName = [
            { "name": "no", "targets": 0 },
            { "name": "product_id", "targets": 1 },
            { "name": "product_desc", "targets": 2 },
            { "name": "brand", "targets": 3 },
            { "name": "category", "targets": 4 },
            { "name": "price", "targets": 5 },
            { "name": "supplier", "targets": 6 },
            { "name": "company", "targets": 7 },
            { "name": "active_status", "targets": 8 },
            { "name": "action", "targets": 9 }
        ]
        this.datatableId = '#product_datatable_id'
        this.apiEndpoint = '/product_api'
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
        const get = ( id ) => {
            return document.querySelector( id ).value
        }
        let formValues = {
            product_desc: get( '#productDescFields' ),
            brand: get( '#brandFields' ),
            price: get( '#priceFields' ),
            category: get( '#categoryFields' ),
            supplier: get( '#supplierFields' ),
            company: get( '#companyFields' )
        }
        return formValues
    }
    getDeleteFormValues() {
        let formValues = {
            product_id: document.getElementById( 'delete_confirm_massage_id' ).value
        }
        return formValues
    }
    getUpdateFormValues() {
        const get = ( id ) => {
            return document.querySelector( id ).value
        }
        let formValues = {
            product_id: get( '#productIdFields' ),
            product_desc: get( '#productDescFields' ),
            brand: get( '#brandFields' ),
            price: get( '#priceFields' ),
            category: get( '#categoryFields' ),
            supplier: get( '#supplierFields' ),
            company: get( '#companyFields' ),
            active_status: this.getActiveStatusValue( '#activeStatusFields' )
        }
        return formValues
    }
    setUpdateFormValues( recordValues ) {
        const get = ( id ) => {
            return document.querySelector( id )
        }
        get( '#productIdFields' ).value = recordValues.product_id
        get( '#productDescFields' ).value = recordValues.product_desc
        get( '#brandFields' ).value = recordValues.brand
        get( '#priceFields' ).value = recordValues.price
        get( '#categoryFields' ).value = recordValues.category
        get( '#supplierFields' ).value = recordValues.supplier
        get( '#companyFields' ).value = recordValues.company
        get( '#activeStatusFields' ).value = recordValues.active_status
        get( '#activeStatusFields' ).checked = recordValues.active_status
    }
}
class FormValidationImpl extends FormValidation {
    constructor() {
        super()
    }
    validateUpdateParams( updateParams ) {
        const validProductId = this.validateProductId( updateParams )
        const sameValidationWithInsert = this.validateInsertParams( updateParams )
        if ( !validProductId.isValid ) return validProductId;
        if ( !sameValidationWithInsert.isValid ) return sameValidationWithInsert;
        return this.validateResult( 'Data is valid', true )
    }
    validateDeleteParams( deleteParams ) {
        if ( !deleteParams.product_id || deleteParams.product_id.length < 0 ) {
            return this.validateResult( 'Product Id doesnt found' )
        }
        return this.validateResult( 'Data is valid', true )
    }
    validateInsertParams( insertParams ) {
        const validProductDesc = this.validateProductDesc( insertParams )
        const validBrand = this.validateBrand( insertParams )
        const validPrice = this.validatePrice( insertParams )
        const validCategory = this.validateCategory( insertParams )
        const validSupplier = this.validateSupplier( insertParams )
        const validCompany = this.validateCompany( insertParams )

        if ( !validProductDesc.isValid ) return validProductDesc;
        if ( !validBrand.isValid ) return validBrand;
        if ( !validPrice.isValid ) return validPrice;
        if ( !validCategory.isValid ) return validCategory;
        if ( !validSupplier.isValid ) return validSupplier;
        if ( !validCompany.isValid ) return validCompany;
        return this.validateResult( 'Data is valid', true )
    }
    validateProductDesc( formData ) {
        if ( !formData.product_desc ) {
            return this.validateResult( 'Product Description is empty' )
        }
        if ( formData.product_desc.length < 3 ) {
            return this.validateResult( 'Product Description too short' )
        }
        if ( formData.product_desc.length > 500 ) {
            return this.validateResult( 'Product Description too long' )
        }
        return this.validateResult( 'Data is valid', true )
    }
    validateBrand( formData ) {
        if ( !formData.brand ) {
            return this.validateResult( 'Brand is empty' )
        }
        if ( formData.brand.length < 3 ) {
            return this.validateResult( 'Brand is too short' )
        }
        if ( formData.brand.length > 100 ) {
            return this.validateResult( 'Brand is too long' )
        }
        return this.validateResult( 'Data is valid', true )
    }
    validatePrice( formData ) {
        if ( !formData.price ) {
            return this.validateResult( 'Price is empty' )
        }
        if ( isNaN( formData.price ) ) {
            return this.validateResult( 'Price must be a number' )
        }
        if ( formData.price < 1 ) {
            return this.validateResult( 'Price must be greater than 0' )
        }
        if ( formData.price.toString().length > 12 ) {
            return this.validateResult( 'Price is too long' )
        }
        return this.validateResult( 'Data is valid', true )
    }
    validateCategory( formData ) {
        if ( !formData.category ) {
            return this.validateResult( 'Category product is not selected' )
        }
        if ( isNaN( formData.category ) ) {
            return this.validateResult( 'Category product is not valid' )
        }
        return this.validateResult( 'Data is valid', true )
    }
    validateSupplier( formData ) {
        if ( !formData.category ) {
            return this.validateResult( 'Supplier  is not selected' )
        }
        if ( isNaN( formData.category ) ) {
            return this.validateResult( 'Supplier is not valid' )
        }
        return this.validateResult( 'Data is valid', true )
    }
    validateProductId( formData ) {
        if ( !formData.product_id ) {
            return this.validateResult( 'Product id is empty' )
        }
        if ( isNaN( formData.product_id ) ) {
            return this.validateResult( 'Product id is not valid' )
        }
        return this.validateResult( 'Data is valid', true )
    }
    validateCompany( formData ) {
        if ( !formData.company ) {
            return this.validateResult( 'Company  is not selected' )
        }
        if ( isNaN( formData.company ) ) {
            return this.validateResult( 'Company is not valid' )
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
        const confirmMessage = `Area you sure to delete ${ formValues.product_id } - ${ formValues.product_desc } ?`
        document.getElementById( 'delete_confirm_massage_id' ).innerHTML = confirmMessage
        document.getElementById( 'delete_confirm_massage_id' ).value = formValues.product_id
    }
    clearAddNewDataForm() {
        const get = ( id ) => {
            return document.querySelector( id )
        }
        get( '#productDescFields' ).value = ''
        get( '#brandFields' ).value = ''
        get( '#priceFields' ).value = ''
        get( '#categoryFields' ).value = ''
        get( '#supplierFields' ).value = ''
        get( '#companyFields' ).value = ''
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
                new DatatableProductImpl().reloadDatatable()
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
        this.sendAjax( { url: '/product_api', payload: payload }, ajaxCallback )
    }
    getSingleData( recordId ) {
        const payload = this.createPayload( 'POST', { 'product_id': recordId } )
        const onSuccess = ( response ) => {
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
        this.sendAjax( { url: '/product_api_search', payload: payload }, ajaxCallback )
    }
    getSingleDataForDeleteActions( recordId ) {
        const payload = this.createPayload( 'POST', { 'product_id': recordId } )
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
        this.sendAjax( { url: '/product_api_search', payload: payload }, ajaxCallback )

    }
    updateData( formData ) {
        const payload = this.createPayload( 'PUT', formData )
        const onSuccess = ( response ) => {
            if ( !response.status ) {
                return new Alert().failedAjax( response.msg )
            }
            new Alert().successAjax( response.msg )
            new DatatableProductImpl().reloadDatatable()
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
        this.sendAjax( { url: '/product_api', payload: payload }, ajaxCallback )

    }
    deleteData( formData ) {
        const payload = this.createPayload( 'DELETE', formData )
        const onSuccess = ( response ) => {
            if ( !response.status ) {
                return new Alert().failedAjax( response.msg )
            }
            new Alert().successAjax( response.msg )
            new DatatableProductImpl().reloadDatatable()
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

        this.sendAjax( { url: '/product_api', payload: payload }, ajaxCallback )
    }
}

const runScript = () => {
    $( document ).ready( function () {
        const modalForm = new ModalFormImpl()
        new DatatableProductImpl().initiateDatatable()
        modalForm.registerOnHideModal()
        modalForm.disabledBtnNewDataOnClick()
        new ButtonEventImpl().bindEventWithAjax()
    } )
}

runScript()
