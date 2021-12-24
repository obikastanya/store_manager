class DatatableSupplierImpl extends BaseDatatable {
    constructor() {
        super()
        this.tableColumns = [
            {
                data: null,
                defaultContent: ''
            },
            { data: 'supplier_id' },
            { data: 'supplier' },
            { data: 'phone_number' },
            { data: 'address' },
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
                    return this.buttonEdit.replace( "_data_", data.supplier_id ) + '&nbsp;' + this.buttonDelete.replace( "_data_", data.supplier_id )
                }
            }
        ]
        this.columnName = [
            { "name": "no", "targets": 0 },
            { "name": "supplier_id", "targets": 1 },
            { "name": "supplier", "targets": 2 },
            { "name": "phone_number", "targets": 3 },
            { "name": "address", "targets": 4 },
            { "name": "active_status", "targets": 5 },
            { "name": "action", "targets": 6 }
        ]
        this.datatableId = '#supplier_datatable_id'
        this.apiEndpoint = '/supplier_api'
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
            supplier: document.querySelector( '#supplierFields' ).value,
            phone_number: document.querySelector( '#phoneNumberFields' ).value,
            address: document.querySelector( '#addressFields' ).value

        }
        return formValues
    }
    getDeleteFormValues() {
        let formValues = {
            supplier_id: document.getElementById( 'delete_confirm_massage_id' ).value
        }
        return formValues
    }
    getUpdateFormValues() {
        let formValues = {
            supplier_id: document.querySelector( '#idSupplierFields' ).value,
            supplier: document.querySelector( '#supplierUpdateFields' ).value,
            phone_number: document.querySelector( '#phoneNumberUpdateFields' ).value,
            address: document.querySelector( '#addressUpdateFields' ).value,
            active_status: this.getActiveStatusValue( '#activeStatusFields' )
        }
        return formValues
    }
    setUpdateFormValues( recordValues ) {
        document.querySelector( '#idSupplierFields' ).value = recordValues.supplier_id
        document.querySelector( '#supplierUpdateFields' ).value = recordValues.supplier
        document.querySelector( '#phoneNumberUpdateFields' ).value = recordValues.phone_number
        document.querySelector( '#addressUpdateFields' ).value = recordValues.address
        document.querySelector( '#activeStatusFields' ).checked = recordValues.active_status
        document.querySelector( '#activeStatusFields' ).value = recordValues.active_status
    }
}
class FormValidationImpl extends FormValidation {
    constructor() {
        super()
    }
    validateUpdateParams( updateParams ) {
        const validIdSupplier = this.validateIdSupplier( updateParams )
        const sameValidationWithInsert = this.validateInsertParams( updateParams )
        const validActiveStatus = this.validateActiveStatus( updateParams )

        if ( !validIdSupplier.isValid ) return validIdSupplier;
        if ( !sameValidationWithInsert.isValid ) return sameValidationWithInsert;
        if ( !validActiveStatus.isValid ) return validActiveStatus;
        return this.validateResult( 'Data is valid', true )
    }
    validateDeleteParams( deleteParams ) {
        if ( !deleteParams.supplier_id || deleteParams.supplier_id.length < 0 ) {
            return this.validateResult( 'Supplier Code doesnt found' )
        }
        return this.validateResult( 'Data is valid', true )
    }
    validateInsertParams( insertParams ) {
        const validSupplier = this.validateSupplier( insertParams )
        const validPhoneNumber = this.validatePhoneNumber( insertParams )
        const validAddress = this.validateAddress( insertParams )


        if ( !validSupplier.isValid ) return validSupplier;
        if ( !validPhoneNumber.isValid ) return validPhoneNumber;
        if ( !validAddress.isValid ) return validAddress;

        return this.validateResult( 'Data is valid', true )
    }
    validateIdSupplier( formData ) {
        if ( !formData.supplier_id || formData.supplier_id.length < 0 ) {
            return this.validateResult( 'There is no supplier to update' )
        }
        return this.validateResult( 'Data is valid', true )
    }
    validateSupplier( formData ) {
        if ( !formData.supplier ) {
            return this.validateResult( 'Supplier name is empty' )
        }
        if ( formData.supplier.length < 3 ) {
            return this.validateResult( 'Supplier name too short' )
        }
        if ( formData.supplier.length > 200 ) {
            return this.validateResult( 'Supplier name too long' )
        }
        return this.validateResult( 'Data is valid', true )
    }
    validatePhoneNumber( formData ) {
        if ( !formData.phone_number ) {
            return this.validateResult( 'Phone number is empty' )
        }
        if ( formData.phone_number.toString().length < 3 ) {
            return this.validateResult( 'Phone number is too short' )
        }
        if ( formData.phone_number.toString().length > 15 ) {
            return this.validateResult( 'Phone number is too long' )
        }
        return this.validateResult( 'Data is valid', true )
    }
    validateAddress( formData ) {
        if ( !formData.address ) {
            return this.validateResult( 'Address is empty' )
        }
        if ( formData.address.length < 5 ) {
            return this.validateResult( 'Address is too short' )
        }
        if ( formData.address.length > 300 ) {
            return this.validateResult( 'Address is too long' )
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
        const confirmMessage = `Area you sure to delete ${ formValues.supplier_id } - ${ formValues.supplier } ?`
        document.getElementById( 'delete_confirm_massage_id' ).innerHTML = confirmMessage
        document.getElementById( 'delete_confirm_massage_id' ).value = formValues.supplier_id
    }
    clearAddNewDataForm() {
        document.querySelector( '#supplierFields' ).value = ''
        document.querySelector( '#phoneNumberFields' ).value = ''
        document.querySelector( '#addressFields' ).value = ''
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
                new DatatableSupplierImpl().reloadDatatable()
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
        this.sendAjax( { url: '/supplier_api', payload: payload }, ajaxCallback )
    }
    getSingleData( recordId ) {
        const payload = this.createPayload( 'POST', { 'supplier_id': recordId } )
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
        this.sendAjax( { url: '/supplier_api_search', payload: payload }, ajaxCallback )
    }
    getSingleDataForDeleteActions( recordId ) {
        const payload = this.createPayload( 'POST', { 'supplier_id': recordId } )
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
        this.sendAjax( { url: '/supplier_api_search', payload: payload }, ajaxCallback )

    }
    updateData( formData ) {
        const payload = this.createPayload( 'PUT', formData )
        const onSuccess = ( response ) => {
            if ( !response.status ) {
                return new Alert().failedAjax( response.msg )
            }
            new Alert().successAjax( response.msg )
            new DatatableSupplierImpl().reloadDatatable()
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
        this.sendAjax( { url: '/supplier_api', payload: payload }, ajaxCallback )

    }
    deleteData( formData ) {
        const payload = this.createPayload( 'DELETE', formData )
        const onSuccess = ( response ) => {
            if ( !response.status ) {
                return new Alert().failedAjax( response.msg )
            }
            new Alert().successAjax( response.msg )
            new DatatableSupplierImpl().reloadDatatable()
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

        this.sendAjax( { url: '/supplier_api', payload: payload }, ajaxCallback )
    }
}

const runScript = () => {
    $( document ).ready( function () {
        const modalForm = new ModalFormImpl()
        new DatatableSupplierImpl().initiateDatatable()
        modalForm.registerOnHideModal()
        modalForm.disabledBtnNewDataOnClick()
        new ButtonEventImpl().bindEventWithAjax()
    } )
}

runScript()
