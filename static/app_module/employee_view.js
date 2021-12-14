class DatatableEmployeeImpl extends BaseDatatable {
    constructor() {
        super()
        this.tableColumns = [
            {
                data: null,
                defaultContent: ''
            },
            { data: 'employee_id' },
            { data: 'name' },
            { data: 'position' },
            { data: 'phone_number' },
            { data: 'email' },
            { data: 'address' },
            { data: 'salary' },
            { data: 'employee_status' },
            { data: 'start_working' },
            { data: 'end_working' },
            {
                data: null,
                render: ( data ) => {
                    return this.buttonEdit.replace( "_data_", data.employee_id ) + '&nbsp;' + this.buttonDelete.replace( "_data_", data.employee_id )
                }
            }
        ]
        this.columnName = [
            { name: "no", targets: 0 },
            { name: 'employee_id', targets: 1 },
            { name: 'name', targets: 2 },
            { name: 'position', targets: 3 },
            { name: 'phone_number', targets: 4 },
            { name: 'email', targets: 5 },
            { name: 'address', targets: 6 },
            { name: 'sallary', targets: 7 },
            { name: 'employee_status', targets: 8 },
            { name: 'start_working', targets: 9 },
            { name: 'end_working', targets: 10 },
            { name: 'action', targets: 11 },
        ]
        this.datatableId = '#employee_datatable_id'
        this.apiEndpoint = '/employee_api'
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
            company: document.querySelector( '#companyFields' ).value
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
            company: document.querySelector( '#companyFieldsUpdate' ).value,
            company_id: document.querySelector( '#idCompanyFields' ).value,
            active_status: this.getActiveStatusValue( '#activeStatusFields' )
        }
        return formValues
    }
    setUpdateFormValues( recordValues ) {
        document.querySelector( '#idCompanyFields' ).value = recordValues.company_id
        document.querySelector( '#companyFieldsUpdate' ).value = recordValues.company
        document.querySelector( '#activeStatusFields' ).checked = recordValues.active_status
        document.querySelector( '#activeStatusFields' ).value = recordValues.active_status
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
        document.querySelector( '#companyFields' ).value = ''
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
                new DatatableEmployeeImpl().reloadDatatable()
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
        this.sendAjax( { url: '/company_api', payload: payload }, ajaxCallback )
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
        this.sendAjax( { url: '/company_api_search', payload: payload }, ajaxCallback )
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
        this.sendAjax( { url: '/company_api_search', payload: payload }, ajaxCallback )

    }
    updateData( formData ) {
        const payload = this.createPayload( 'PUT', formData )
        const onSuccess = ( response ) => {
            if ( !response.status ) {
                return new Alert().failedAjax( response.msg )
            }
            new Alert().successAjax( response.msg )
            new DatatableEmployeeImpl().reloadDatatable()
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
        this.sendAjax( { url: '/company_api', payload: payload }, ajaxCallback )

    }
    deleteData( formData ) {
        const payload = this.createPayload( 'DELETE', formData )
        const onSuccess = ( response ) => {
            if ( !response.status ) {
                return new Alert().failedAjax( response.msg )
            }
            new Alert().successAjax( response.msg )
            new DatatableEmployeeImpl().reloadDatatable()
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

        this.sendAjax( { url: '/company_api', payload: payload }, ajaxCallback )
    }
}

const runScript = () => {
    $( document ).ready( function () {
        const modalForm = new ModalFormImpl()
        new DatatableEmployeeImpl().initiateDatatable()
        modalForm.registerOnHideModal()
        modalForm.disabledBtnNewDataOnClick()
        new ButtonEventImpl().bindEventWithAjax()
    } )
}

runScript()
