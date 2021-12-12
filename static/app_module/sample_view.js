class DatatableCompanyImpl extends BaseDatatable {
    constructor() {
        super()
        this.tableColumns = []
        this.columnName = []
        this.datatableId = ''
        this.apiEndpoint = ''
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
    getAddNewDataFormValues() { }
    getDeleteFormValues() { }
    getUpdateFormValues() { }
    setUpdateFormValues( recordValues ) { }
}
class FormValidationImpl extends FormValidation {
    constructor() {
        super()
    }
    validateUpdateParams( updateParams ) { }
    validateDeleteParams( deleteParams ) { }
    validateInsertParams( insertParams ) { }
    validateCompany( formData ) { }
    validateIdCompany( formData ) { }
    validateActiveStatus( formData ) { }
    validateResult( message = '', isValid = false ) {
        return { isValid: isValid, message: message }
    }
}
class ModalFormImpl extends ModalForm {
    constructor() {
        super()
    }
    setDeleteConfirmMessage( formValues ) { }
    clearAddNewDataForm() { }
}

class ButtonEventImpl extends ButtonEvent {
    constructor() {
        super()
    }
    saveNewData() { }
    saveUpdatedData() { }
    deleteData() { }
}
class AjaxImpl extends Ajax {
    constructor() {
        super()
    }
    saveNewRecord( formData ) {
        const payload = this.createPayload( 'POST', formData )
        pr
        const onSuccess = ( response ) => { }
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
    getSingleData( recordId ) { }
    getSingleDataForDeleteActions( recordId ) { }
    updateData( formData ) { }
    deleteData( formData ) { }
}

const runScript = () => {
    $( document ).ready( function () {
        const modalForm = new ModalFormImpl()
        new DatatableCompanyImpl().initiateDatatable()
        modalForm.registerOnHideModal()
        modalForm.disabledBtnNewDataOnClick()
        new ButtonEventImpl().bindEventWithAjax()
    } )
}

runScript()
