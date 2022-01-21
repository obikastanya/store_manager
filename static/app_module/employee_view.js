
const runScript = () => {
    $( document ).ready( function () {
        const modalForm = new ModalFormImpl()
        new DatatableEmployeeImpl().initiateDatatable()
        new AjaxImpl().getOptionForEmployeeStatusMaster()
        modalForm.registerOnHideModal()
        modalForm.disabledBtnNewDataOnClick()

        const btnEvent = new ButtonEventImpl()
        btnEvent.bindEventWithAjax()
        btnEvent.setMasterAsActiveMenu()
    } )
}

runScript()


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
        this.sendAjax( { url: '/employee_api', payload: payload }, ajaxCallback )
    }
    getSingleData( recordId ) {
        const payload = this.createPayload( 'POST', { 'employee_id': recordId } )
        const onSuccess = ( response ) => {
            console.log( response )
            if ( !response.data.length ) new Alert().failedAjax( response.msg );
            new FormDataImpl().setUpdateFormValues( response.data[ 0 ] )
            return
        }
        const ajaxCallback = {
            onSuccess: onSuccess,
            onFail: ( error ) => {
                new Alert().error()
            },
            onFinal: () => { }
        }
        this.sendAjax( { url: '/employee_api_search', payload: payload }, ajaxCallback )
    }
    getSingleDataForDeleteActions( recordId ) {
        const payload = this.createPayload( 'POST', { 'employee_id': recordId } )
        const onSuccess = ( response ) => {
            if ( !response.data.length ) new Alert().failedAjax( response.msg );
            new ModalFormImpl().setDeleteConfirmMessage( response.data[ 0 ] )
            return
        }
        const ajaxCallback = {
            onSuccess: onSuccess,
            onFail: ( error ) => {
                new Alert().error()
            },
            onFinal: () => { }
        }
        this.sendAjax( { url: '/employee_api_search', payload: payload }, ajaxCallback )

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
        this.sendAjax( { url: '/employee_api', payload: payload }, ajaxCallback )

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

        this.sendAjax( { url: '/employee_api', payload: payload }, ajaxCallback )
    }
    getOptionForEmployeeStatusMaster() {
        const onSuccess = ( response ) => {
            new FormDataImpl().setOptionForEmployeeStatusMaster( response.data )
        }
        const ajaxCallback = {
            onSuccess: onSuccess,
            onFail: ( err ) => { console.log( err ) }
        }
        fetch( '/employee_status_lov_api' )
            .then( response => response.json() )
            .then( onSuccess )
            .catch( ajaxCallback.onFail )

    }
}

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
            {
                data: 'employee_status', render: ( data ) => {
                    return data.employee_status
                }
            },
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
        const get = ( idElement ) => {
            return document.querySelector( idElement ).value
        }
        let formValues = {
            employee_status_id: get( '#employeStatusFields' ),
            name: get( '#nameFields' ),
            phone_number: get( '#phoneNumberFields' ),
            email: get( '#emailFields' ),
            address: get( '#addressFields' ),
            salary: get( '#salaryFields' ),
            position: get( '#positionFields' ),
            start_working: get( '#startWorkingFields' )
        }
        return formValues
    }
    getDeleteFormValues() {
        let formValues = {
            employee_id: document.getElementById( 'delete_confirm_massage_id' ).value
        }
        return formValues
    }
    getUpdateFormValues() {
        const get = ( id ) => {
            return document.querySelector( id ).value
        }
        let formValues = {
            employee_id: get( '#employeeIdFields' ),
            employee_status_id: get( '#employeStatusUpdateFields' ),
            name: get( '#nameUpdateFields' ),
            phone_number: get( '#phoneNumberUpdateFields' ),
            email: get( '#emailUpdateFields' ),
            address: get( '#addressUpdateFields' ),
            salary: get( '#salaryUpdateFields' ),
            position: get( '#positionUpdateFields' ),
            start_working: get( '#startWorkingUpdateFields' ),
            end_working: get( '#endWorkingFields' )
        }
        return formValues
    }
    setUpdateFormValues( recordValues ) {
        const get = ( id ) => {
            return document.querySelector( id )
        }
        get( '#employeeIdFields' ).value = recordValues.employee_id
        get( '#employeStatusUpdateFields' ).value = recordValues.employee_status.employee_status_id
        get( '#nameUpdateFields' ).value = recordValues.name
        get( '#phoneNumberUpdateFields' ).value = recordValues.phone_number
        get( '#emailUpdateFields' ).value = recordValues.email
        get( '#addressUpdateFields' ).value = recordValues.address
        get( '#salaryUpdateFields' ).value = recordValues.salary
        get( '#positionUpdateFields' ).value = recordValues.position
        get( '#startWorkingUpdateFields' ).value = recordValues.start_working
        get( '#endWorkingFields' ).value = recordValues.end_working
    }
    generateOption( recordValues ) {
        let options = ''
        for ( const values of recordValues ) {
            options += ` <option value=${ values.employee_status_id }>${ values.employee_status }</option> `
        }
        return options
    }

    setOptionForEmployeeStatusMaster( recordValues ) {
        // some dom manipulation
        // setOptionForEmployeeStatusMaster
        for ( const id of [ '#employeStatusUpdateFields', '#employeStatusFields' ] ) {
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
        const validEmployeeId = this.validateEmployeeId( updateParams )
        const validEmployeeData = this.validateInsertParams( updateParams )

        if ( !validEmployeeId.isValid ) return validEmployeeId;
        if ( !validEmployeeData.isValid ) return validEmployeeData
        return this.validateResult( 'Data is valid', true )
    }
    validateDeleteParams( deleteParams ) {
        if ( !deleteParams.employee_id || deleteParams.employee_id.length < 0 ) {
            return this.validateResult( 'Employee Id doesnt found' )
        }
        return this.validateResult( 'Data is valid', true )
    }
    validateInsertParams( insertParams ) {
        // check all  data, is valid or not
        const validEmployeeStatusId = this.validateEmployeeStatusId( insertParams )
        const validName = this.validateName( insertParams )
        const validPhoneNumber = this.validatePhoneNumber( insertParams )
        const validEmail = this.validateEmail( insertParams )
        const validAddress = this.validateAddress( insertParams )
        const validSalary = this.validateSalary( insertParams )
        const validPosition = this.validatePosition( insertParams )
        const validStartWorking = this.validStartWorking( insertParams )

        // return status and massage from validation if the validation isValid is false        
        if ( !validName.isValid ) return validName;
        if ( !validPosition.isValid ) return validPosition;
        if ( !validPhoneNumber.isValid ) return validPhoneNumber;
        if ( !validEmail.isValid ) return validEmail;
        if ( !validAddress.isValid ) return validAddress;
        if ( !validSalary.isValid ) return validSalary;
        if ( !validEmployeeStatusId.isValid ) return validEmployeeStatusId;
        if ( !validStartWorking.isValid ) return validStartWorking;
        return this.validateResult( 'Data is valid', true )
    }
    validateEmployeeId( formData ) {
        if ( !formData.employee_id ) {
            return this.validateResult( 'Employee id is empty' )
        }
        if ( isNaN( formData.employee_id ) ) {
            return this.validateResult( 'Invalid employee id' )
        }
        return this.validateResult( 'Data is valid', true )
    }
    validateEmployeeStatusId( formData ) {
        if ( !formData.employee_status_id ) {
            return this.validateResult( 'Employee status id is empty' )
        }
        if ( isNaN( formData.employee_status_id ) ) {
            return this.validateResult( 'Invalid employee status id' )
        }
        if ( ( formData.employee_status_id ).toString().length > 1 ) {
            return this.validateResult( 'Invalid employee status id' )
        }
        return this.validateResult( 'Data is valid', true )
    }
    validateName( formData ) {
        if ( !formData.name ) {
            return this.validateResult( 'Employee name is empty' )
        }
        if ( formData.name.length < 3 ) {
            return this.validateResult( 'Name minimun character is 3' )
        }
        if ( formData.name.length > 200 ) {
            return this.validateResult( 'Name is too long' )
        }
        return this.validateResult( 'Data is valid', true )
    }
    validatePhoneNumber( formData ) {
        if ( !formData.phone_number ) {
            return this.validateResult( 'Phone number is empty' )
        }
        if ( ( formData.phone_number ).toString().length < 3 ) {
            return this.validateResult( 'Phone number minimum character is 3' )
        }
        if ( ( formData.phone_number ).toString().length > 30 ) {
            return this.validateResult( 'Phone number is too long' )
        }
        if ( isNaN( formData.phone_number ) ) {
            return this.validateResult( 'Phone number is too long' )
        }
        return this.validateResult( 'Data is valid', true )
    }
    validateEmail( formData ) {
        if ( !formData.email ) {
            return this.validateResult( 'Email is empty' )
        }
        if ( !this.isMatchEmailPattern( formData.email ) ) {
            return this.validateResult( 'Invalid email format' )
        }
        if ( formData.email.length > 100 ) {
            return this.validateResult( 'Email is too long' )
        }
        return this.validateResult( 'Data is valid', true )
    }
    validateAddress( formData ) {
        console.log( formData )
        if ( !formData.address ) {
            return this.validateResult( 'Address is empty' )
        }
        if ( formData.address.length < 3 ) {
            return this.validateResult( 'Address is too short' )
        }
        if ( formData.address.length > 200 ) {
            return this.validateResult( 'Address is too long' )
        }
        return this.validateResult( 'Data is valid', true )
    }
    validateSalary( formData ) {
        if ( ( formData.salary ).toString().length < 3 ) {
            return this.validateResult( 'Minimum salary is 3 digit' )
        }
        if ( ( formData.salary ).toString().length > 12 ) {
            return this.validateResult( 'Salary is too long' )
        }
        if ( isNaN( formData.salary ) ) {
            return this.validateResult( 'Invalid salary' )
        }
        return this.validateResult( 'Data is valid', true )
    }
    validatePosition( formData ) {
        if ( !formData.position ) {
            return this.validateResult( 'Employee position is empty' )
        }
        if ( formData.position.length < 3 ) {
            return this.validateResult( 'Position Name minimun character is 3' )
        }
        if ( formData.position.length > 100 ) {
            return this.validateResult( 'Position is too long' )
        }
        return this.validateResult( 'Data is valid', true )
    }
    validStartWorking( formData ) {
        if ( !formData.start_working ) {
            return this.validateResult( 'Start working is empty' )
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
    isMatchEmailPattern( email ) {
        var emailPattern = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/;
        return emailPattern.test( email );
    }
}
class ModalFormImpl extends ModalForm {
    constructor() {
        super()
    }
    setDeleteConfirmMessage( formValues ) {
        const confirmMessage = `Area you sure to delete  (${ formValues.employee_id }) ${ formValues.name } ?`
        document.getElementById( 'delete_confirm_massage_id' ).innerHTML = confirmMessage
        document.getElementById( 'delete_confirm_massage_id' ).value = formValues.employee_id
    }
    clearAddNewDataForm() {
        const get = ( id ) => {
            return document.querySelector( id )
        }
        get( '#employeStatusFields' ).value = ''
        get( '#nameFields' ).value = ''
        get( '#phoneNumberFields' ).value = ''
        get( '#emailFields' ).value = ''
        get( '#addressFields' ).value = ''
        get( '#salaryFields' ).value = ''
        get( '#positionFields' ).value = ''
        get( '#startWorkingFields' ).value = ''
    }
}
