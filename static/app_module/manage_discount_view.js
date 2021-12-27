class DatatableDiscountAppliedImpl extends BaseDatatable {
    constructor() {
        super()
        this.tableColumns = [
            {
                data: null,
                defaultContent: ''
            },
            {
                data: 'discount_product', render: ( data ) => {
                    return data.product_id
                }
            },
            {
                data: 'discount_product', render: ( data ) => {
                    return data.product_desc
                }
            },
            {
                data: 'discount_master', render: ( data ) => {
                    return data.desc
                }
            },
            {
                data: 'discount_master', render: ( data ) => {
                    return data.discount_type.discount_type
                }
            },
            { data: 'start_date' },
            { data: 'expired_date' },
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
                    const strIdProductAndDiscount = `${ data.discount_product.product_id },${ data.discount_master.discount_id }`
                    return this.buttonEdit.replace( "_data_", strIdProductAndDiscount ) + '&nbsp;' + this.buttonDelete.replace( "_data_", strIdProductAndDiscount )
                }
            }
        ]
        this.columnName = [
            { "name": "no", "targets": 0 },
            { "name": "product_id", "targets": 1 },
            { "name": "product_desc", "targets": 2 },
            { "name": "discount_desc", "targets": 3 },
            { "name": "discount_type", "targets": 4 },
            { "name": "start_date", "targets": 5 },
            { "name": "expired_date", "targets": 6 },
            { "name": "active_status", "targets": 7 },
            { "name": "action", "targets": 8 }
        ]
        this.datatableId = '#discount_applied_datatable_id'
        this.apiEndpoint = '/manage_discount_api'
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
            company_id: document.getElementById( 'delete_confirm_massage_id' ).value
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
        if ( !deleteParams.company_id || deleteParams.company_id.length < 0 ) {
            return this.validateResult( 'Company Id doesnt found' )
        }
        return this.validateResult( 'Data is valid', true )
    }
    validateInsertParams( insertParams ) {
        const validIdProduct = this.validateIdProduct( insertParams )
        console.log( 'p', validIdProduct )
        const validIdDiscount = this.validateIdDiscount( insertParams )
        const validStartDate = this.validateStartDate( insertParams )
        const validExpiredDate = this.validateExpiredDate( insertParams )

        if ( !validIdProduct.isValid ) return validIdProduct;
        if ( !validIdDiscount.isValid ) return validIdDiscount;
        if ( !validStartDate.isValid ) return validStartDate;
        if ( !validExpiredDate.isValid ) return validExpiredDate;
        return this.validateResult( 'Data is valid', true )
    }
    validateIdProduct( formData ) {
        if ( isNaN( formData.product_id ) ) {
            return this.validateResult( 'Invalid Product selected' )
        }
        if ( !( parseInt( formData.product_id ) ) ) {
            return this.validateResult( 'Invalid Product selected' )
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
    setDeleteConfirmMessage( formValues ) {
        console.log( formValues )
        const confirmMessage = `Area you sure to delete discount applied on ${ formValues.product_desc } ?`
        document.getElementById( 'delete_confirm_massage_id' ).innerHTML = confirmMessage
        document.getElementById( 'delete_confirm_massage_id' ).value = formValues.product_id
    }
    clearAddNewDataForm() {
        document.querySelector( '#productIdFields' ).value = ''
        document.querySelector( '#discountIdFields' ).value = ''
        document.querySelector( '#startDateFields' ).value = ''
        document.querySelector( '#expiredDateFields' ).value = ''
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
                new DatatableDiscountAppliedImpl().reloadDatatable()
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
        this.sendAjax( { url: '/manage_discount_api', payload: payload }, ajaxCallback )
    }
    getSingleData( recordId ) {
        const params = {
            product_id: recordId.split( ',' )[ 0 ],
            discount_id: recordId.split( ',' )[ 1 ]
        }
        const payload = this.createPayload( 'POST', params )
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
        this.sendAjax( { url: '/manage_discount_api_search', payload: payload }, ajaxCallback )
    }
    getSingleDataForDeleteActions( recordId ) {
        const params = {
            product_id: recordId.split( ',' )[ 0 ],
            discount_id: recordId.split( ',' )[ 1 ]
        }
        const payload = this.createPayload( 'POST', params )
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
        this.sendAjax( { url: '/manage_discount_api_search', payload: payload }, ajaxCallback )

    }
    updateData( formData ) {
        const payload = this.createPayload( 'PUT', formData )
        const onSuccess = ( response ) => {
            if ( !response.status ) {
                return new Alert().failedAjax( response.msg )
            }
            new Alert().successAjax( response.msg )
            new DatatableDiscountAppliedImpl().reloadDatatable()
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
        this.sendAjax( { url: '/manage_discount_api', payload: payload }, ajaxCallback )

    }
    deleteData( formData ) {
        const payload = this.createPayload( 'DELETE', formData )
        const onSuccess = ( response ) => {
            if ( !response.status ) {
                return new Alert().failedAjax( response.msg )
            }
            new Alert().successAjax( response.msg )
            new DatatableDiscountAppliedImpl().reloadDatatable()
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

        this.sendAjax( { url: '/manage_discount_api', payload: payload }, ajaxCallback )
    }
    getOption( endPoint, onSuccess = () => { } ) {
        fetch( endPoint )
            .then( response => response.json() )
            .then( onSuccess )
            .catch( ( err ) => { console.log( err ) } )
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
            const selectFieldIds = [ '#productIdUpdateFields', '#productIdFields' ]
            new FormDataImpl().setOptionForSelectFields( selectFieldIds, newRecordValues )
        }
        this.getOption( 'product_lov_api', onSuccess )
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
            const selectFieldIds = [ '#discountIdUpdateFields', '#discountIdFields' ]
            new FormDataImpl().setOptionForSelectFields( selectFieldIds, newRecordValues )
        }
        this.getOption( 'discount_lov_api', onSuccess )
    }
    getLovForSelectField() {
        this.getLovForProductFields()
        this.getLovForDiscountFields()
    }
}

const runScript = () => {
    $( document ).ready( function () {
        const modalForm = new ModalFormImpl()
        new DatatableDiscountAppliedImpl().initiateDatatable()
        new AjaxImpl().getLovForSelectField()
        modalForm.registerOnHideModal()
        modalForm.disabledBtnNewDataOnClick()
        new ButtonEventImpl().bindEventWithAjax()
    } )
}

runScript()
