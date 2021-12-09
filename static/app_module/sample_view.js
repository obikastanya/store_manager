// sample 
class DatatableCompanyImpl extends BaseDatatable{
    constructor() {
        super()
        this.columnName = []
        this.tableColumns = []
        this.datatableId = ''
        this.apiEndpoint = '/'
        this.AjaxInstance = undefined
        this.textModalFormClass = 'new ModalForm()'
    }
}
class FormDataImpl extends FormData {
    saveNewRecord( formData ) { }
    getSingleData( recordId ) { }
    getSingleDataForDeleteActions( recordId ) { }
    updateData( formData ) { }
    deleteData( formData ) { }
}
class AjaxImpl extends Ajax{
    saveNewRecord( formData ) { }
    getSingleData( recordId ) { }
    getSingleDataForDeleteActions( recordId ) { }
    updateData( formData ) { }
    deleteData( formData ) { }
}
class FormValidationImpl extends FormValidation{
    validateUpdateParams( updateParams ) { }
    validateDeleteParams( deleteParams ) { }
    validateInsertParams( insertParams ) { }
}
class ModalFormImpl extends ModalForm{
    setDeleteConfirmMessage( formValues ) { }
    clearAddNewDataForm() { }
}

const runScript = () => {
    $( document ).ready( function () {
        const modalForm = new ModalFormImpl()
        new DatatableCompanyImpl().initiateDatatable()
        modalForm.registerOnHideModal()
        modalForm.disabledBtnNewDataOnClick()
        new ModalButtonEvent().bindEventWithAjax()
    } )
}

class ButtonEventImpl extends ButtonEvent{
    constructor() {
        super()
        this.FormDataInstance = undefined
        this.FormValidationInstance = undefined
        this.AjaxInstance = undefined
        this.ModalFormInstance = undefined
    }
}
runScript()
