class DatatableDiscountImpl extends BaseDatatable {
    constructor() {
        super()
        this.tableColumns = [
            {
                data: null,
                defaultContent: ''
            },
            { data: 'discount_id' },
            { data: 'discount_type' },
            { data: 'desc' },
            { data: 'discount_nominal' },
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
                    return this.buttonEdit.replace( "_data_", data.discount_id ) + '&nbsp;' + this.buttonDelete.replace( "_data_", data.discount_id )
                }
            }
        ]
        this.columnName = [
            { "name": "no", "targets": 0 },
            { "name": "discount_id", "targets": 1 },
            { "name": "discount_type", "targets": 2 },
            { "name": "discount", "targets": 3 },
            { "name": "nominal", "targets": 4 },
            { "name": "active_status", "targets": 5 },
            { "name": "action", "targets": 6 }
        ]
        this.datatableId = '#discount_datatable_id'
        this.apiEndpoint = '/discount_api'
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
        const formData = {
            discount: document.querySelector( '#discountFields' ).value,
            discount_type: document.querySelector( '#discountTypeFields' ).value,
            nominal: document.querySelector( '#discountNominalFields' ).value,
        }
        return formData
    }
    getDeleteFormValues() {
        let formValues = {
            discount_id: document.getElementById( 'delete_confirm_massage_id' ).value
        }
        return formValues
    }
    getUpdateFormValues() {
        let formValues = {
            discount_id: document.querySelector( '#idDiscountFields' ).value,
            discount: document.querySelector( '#discountUpdateFields' ).value,
            discount_type: document.querySelector( '#discountTypeUpdateFields' ).value,
            nominal: document.querySelector( '#discountNominalUpdateFields' ).value,
            active_status: this.getActiveStatusValue( '#activeStatusFields' )
        }
        return formValues
    }
    setUpdateFormValues( recordValues ) {
        document.querySelector( '#idDiscountFields' ).value = recordValues.discount_id
        document.querySelector( '#discountUpdateFields' ).value = recordValues.desc
        document.querySelector( '#discountTypeUpdateFields' ).value = recordValues.discount_type
        document.querySelector( '#discountNominalUpdateFields' ).value = recordValues.discount_nominal
        document.querySelector( '#activeStatusFields' ).checked = recordValues.active_status
        document.querySelector( '#activeStatusFields' ).value = recordValues.active_status
    }
}
class FormValidationImpl extends FormValidation {
    constructor() {
        super()
    }
    validateUpdateParams( updateParams ) {
        const validDiscountId = this.validateDiscountId( updateParams )
        const validDiscountActiveStatus = this.validateActiveStatus( updateParams )
        // reuse param insert validation because it has the save rules.
        const sameValidationAsInsert = this.validateInsertParams( updateParams )
        if ( !validDiscountId.isValid ) return validDiscountId;
        if ( !validDiscountActiveStatus.isValid ) return validDiscountActiveStatus;
        if ( !sameValidationAsInsert.isValid ) return sameValidationAsInsert;
        return this.validateResult( 'Data is valid', true )
    }
    validateDeleteParams( deleteParams ) {
        console.log( deleteParams )
        if ( !deleteParams.discount_id || deleteParams.discount_id.length < 0 ) {
            return this.validateResult( 'Discount Id doesnt found' )
        }
        return this.validateResult( 'Data is valid', true )
    }
    validateInsertParams( insertParams ) {
        const validDiscountName = this.validateDiscountName( insertParams )
        const validDiscountType = this.validateDiscountType( insertParams )
        const validNominal = this.validateNominal( insertParams )
        if ( !validDiscountName.isValid ) return validDiscountName;
        if ( !validDiscountType.isValid ) return validDiscountType;
        if ( !validNominal.isValid ) return validNominal;
        return this.validateResult( 'Data is valid', true )
    }
    validateDiscountName( formData ) {
        if ( !formData.discount ) {
            return this.validateResult( 'Discount Name is empty' )
        }
        if ( formData.discount.length < 3 ) {
            return this.validateResult( 'Discount Name too short' )
        }
        if ( formData.discount.length > 200 ) {
            return this.validateResult( 'Discount Name too long' )
        }
        return this.validateResult( 'Data is valid', true )
    }
    validateDiscountType( formData ) {
        if ( !formData.discount_type ) {
            return this.validateResult( 'Discount Type is invalid' )
        }
        if ( Number.isNaN( formData.discount_type ) ) {
            return this.validateResult( 'Cant Find Selected Discount Type' )
        }
        return this.validateResult( 'Data is valid', true )
    }
    validateNominal( formData ) {
        if ( !formData.nominal ) {
            return this.validateResult( 'Cant insert data with empty nominal' )
        }
        if ( Number.isNaN( formData.nominal ) ) {
            return this.validateResult( 'Nominal must be a number' )
        }
        if ( formData.nominal < 1 ) {
            return this.validateResult( 'Nominal must be greater than 0' )
        }
        return this.validateResult( 'Data is valid', true )
    }
    validateDiscountId( formData ) {
        if ( !formData.discount_id || formData.discount_id.length < 0 ) {
            return this.validateResult( 'There is no discount id to update' )
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
        const confirmMessage = `Area you sure to delete ${ formValues.discount_id } - ${ formValues.desc } ?`
        document.getElementById( 'delete_confirm_massage_id' ).innerHTML = confirmMessage
        document.getElementById( 'delete_confirm_massage_id' ).value = formValues.discount_id
    }
    clearAddNewDataForm() {
        document.querySelector( '#discountFields' ).value = ''
        document.querySelector( '#discountTypeFields' ).value = ''
        document.querySelector( '#discountNominalFields' ).value = ''
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
        console.log( payload )
        const onSuccess = ( response ) => {
            if ( response.status ) {
                new ModalFormImpl().hideModal( 'id_modal_for_add_new_data' )
                new Alert().successAjax( response.msg )
                new DatatableDiscountImpl().reloadDatatable()
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
        this.sendAjax( { url: '/discount_api', payload: payload }, ajaxCallback )
    }
    getSingleData( recordId ) {
        const payload = this.createPayload( 'POST', { 'discount_id': recordId } )
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
        this.sendAjax( { url: '/discount_api_search', payload: payload }, ajaxCallback )
    }
    getSingleDataForDeleteActions( recordId ) {
        const payload = this.createPayload( 'POST', { 'discount_id': recordId } )
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
        this.sendAjax( { url: '/discount_api_search', payload: payload }, ajaxCallback )

    }
    updateData( formData ) {
        const payload = this.createPayload( 'PUT', formData )
        const onSuccess = ( response ) => {
            if ( !response.status ) {
                return new Alert().failedAjax( response.msg )
            }
            new Alert().successAjax( response.msg )
            new DatatableDiscountImpl().reloadDatatable()
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
        this.sendAjax( { url: '/discount_api', payload: payload }, ajaxCallback )

    }
    deleteData( formData ) {
        const payload = this.createPayload( 'DELETE', formData )
        const onSuccess = ( response ) => {
            if ( !response.status ) {
                return new Alert().failedAjax( response.msg )
            }
            new Alert().successAjax( response.msg )
            new DatatableDiscountImpl().reloadDatatable()
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

        this.sendAjax( { url: '/discount_api', payload: payload }, ajaxCallback )
    }
}

const runScript = () => {
    $( document ).ready( function () {
        const modalForm = new ModalFormImpl()
        new DatatableDiscountImpl().initiateDatatable()
        modalForm.registerOnHideModal()
        modalForm.disabledBtnNewDataOnClick()
        new ButtonEventImpl().bindEventWithAjax()
    } )
}

runScript()
