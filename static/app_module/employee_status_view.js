const runScript = () => {
    $( document ).ready( function () {
        const modalForm = new ModalFormImpl()
        new DatatableEmployeeStatusImpl().initiateDatatable()
        modalForm.registerOnHideModal()
        modalForm.disabledBtnNewDataOnClick()

        const btnEvent = new ButtonEventImpl()
        btnEvent.bindEventWithAjax()
        btnEvent.setMasterAsActiveMenu()
    } )
}

runScript()

class DatatableEmployeeStatusImpl extends BaseDatatable {
    constructor() {
        super()
        this.tableColumns = [
            {
                data: null,
                defaultContent: ''
            },
            { data: 'employee_status_id' },
            { data: 'employee_status' },
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
                    return this.buttonEdit.replace( "_data_", data.employee_status_id ) + '&nbsp;' + this.buttonDelete.replace( "_data_", data.employee_status_id )
                }
            }
        ]
        this.columnName = [
            { "name": "no", "targets": 0 },
            { "name": "employee_status_id", "targets": 1 },
            { "name": "employee_status", "targets": 2 },
            { "name": "active_status", "targets": 3 },
            { "name": "action", "targets": 4 }
        ]
        this.datatableId = '#employee_status_datatable_id'
        this.apiEndpoint = '/employee_status_api'
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
                new DatatableEmployeeStatusImpl().reloadDatatable()
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
        this.sendAjax( { url: '/employee_status_api', payload: payload }, ajaxCallback )
    }
    getSingleData( recordId ) {
        const payload = this.createPayload( 'POST', { 'employee_status_id': recordId } )
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
        this.sendAjax( { url: '/employee_status_api_search', payload: payload }, ajaxCallback )
    }
    getSingleDataForDeleteActions( recordId ) {
        const payload = this.createPayload( 'POST', { 'employee_status_id': recordId } )
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
        this.sendAjax( { url: '/employee_status_api_search', payload: payload }, ajaxCallback )

    }
    updateData( formData ) {
        const payload = this.createPayload( 'PUT', formData )
        const onSuccess = ( response ) => {
            if ( !response.status ) {
                return new Alert().failedAjax( response.msg )
            }
            new Alert().successAjax( response.msg )
            new DatatableEmployeeStatusImpl().reloadDatatable()
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
        this.sendAjax( { url: '/employee_status_api', payload: payload }, ajaxCallback )

    }
    deleteData( formData ) {
        const payload = this.createPayload( 'DELETE', formData )
        const onSuccess = ( response ) => {
            if ( !response.status ) {
                return new Alert().failedAjax( response.msg )
            }
            new Alert().successAjax( response.msg )
            new DatatableEmployeeStatusImpl().reloadDatatable()
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

        this.sendAjax( { url: '/employee_status_api', payload: payload }, ajaxCallback )
    }
}

class FormDataImpl extends FormData {
    constructor() {
        super()
    }
    getAddNewDataFormValues() {
        let formValues = {
            employee_status: document.querySelector( '#employeeStatusFields' ).value
        }
        return formValues
    }
    getDeleteFormValues() {
        let formValues = {
            employee_status_id: document.getElementById( 'delete_confirm_massage_id' ).value
        }
        return formValues
    }
    getUpdateFormValues() {
        let formValues = {
            employee_status: document.querySelector( '#employeeStatusFieldsUpdate' ).value,
            employee_status_id: document.querySelector( '#idEmployeeStatusFields' ).value,
            active_status: this.getActiveStatusValue( '#activeStatusFields' )
        }
        return formValues
    }
    setUpdateFormValues( recordValues ) {
        document.querySelector( '#idEmployeeStatusFields' ).value = recordValues.employee_status_id
        document.querySelector( '#employeeStatusFieldsUpdate' ).value = recordValues.employee_status
        document.querySelector( '#activeStatusFields' ).checked = recordValues.active_status
        document.querySelector( '#activeStatusFields' ).value = recordValues.active_status
    }
}
class FormValidationImpl extends FormValidation {
    constructor() {
        super()
    }
    validateUpdateParams( updateParams ) {
        const validEmployeeStatusId = this.validateEmployeeStatusId( updateParams )
        const validEmployeeStatus = this.validateEmployeeStatus( updateParams )
        const validActiveStatus = this.validateActiveStatus( updateParams )

        if ( !validEmployeeStatusId.isValid ) return validEmployeeStatusId;
        if ( !validEmployeeStatus.isValid ) return validEmployeeStatus;
        if ( !validActiveStatus.isValid ) return validActiveStatus;
        return this.validateResult( 'Data is valid', true )
    }
    validateDeleteParams( deleteParams ) {
        if ( !deleteParams.employee_status_id || deleteParams.employee_status_id.length < 0 ) {
            return this.validateResult( 'Employee status id doesnt found' )
        }
        return this.validateResult( 'Data is valid', true )
    }
    validateInsertParams( insertParams ) {
        return this.validateEmployeeStatus( insertParams )
    }
    validateEmployeeStatus( formData ) {
        if ( !formData.employee_status ) {
            return this.validateResult( 'Cant insert empty data' )
        }
        if ( formData.employee_status.length < 3 ) {
            return this.validateResult( 'Employee Status too short' )
        }
        if ( formData.employee_status.length > 200 ) {
            return this.validateResult( 'Employee Status too long' )
        }
        return this.validateResult( 'Data is valid', true )
    }
    validateEmployeeStatusId( formData ) {
        if ( !formData.employee_status_id || formData.employee_status_id.length < 0 ) {
            return this.validateResult( 'There is no employe status id to update' )
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
        const confirmMessage = `Area you sure to delete ${ formValues.employee_status_id } - ${ formValues.employee_status } ?`
        document.getElementById( 'delete_confirm_massage_id' ).innerHTML = confirmMessage
        document.getElementById( 'delete_confirm_massage_id' ).value = formValues.employee_status_id
    }
    clearAddNewDataForm() {
        document.querySelector( '#employeeStatusFields' ).value = ''
    }
}

