class DatatableCategoryProductImpl extends BaseDatatable {
    constructor() {
        super()
        this.tableColumns = [
            {
                data: null,
                defaultContent: ''
            },
            { data: 'category_id' },
            { data: 'category' },
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
                    return this.buttonEdit.replace( "_data_", data.category_id ) + '&nbsp;' + this.buttonDelete.replace( "_data_", data.category_id )
                }
            }
        ]
        this.columnName = [
            { "name": "no", "targets": 0 },
            { "name": "category_id", "targets": 1 },
            { "name": "category", "targets": 2 },
            { "name": "active_status", "targets": 3 },
            { "name": "action", "targets": 4 }
        ]
        this.datatableId = '#category_product_datatable_id'
        this.apiEndpoint = '/category_product_api'
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
            category: document.querySelector( '#categoryFields' ).value
        }
        return formValues
    }
    getDeleteFormValues() {
        let formValues = {
            category_id: document.getElementById( 'delete_confirm_massage_id' ).value
        }
        return formValues
    }
    getUpdateFormValues() {
        let formValues = {
            category: document.querySelector( '#categoryFieldsUpdate' ).value,
            category_id: document.querySelector( '#idCategoryFields' ).value,
            active_status: this.getActiveStatusValue( '#activeStatusFields' )
        }
        return formValues
    }
    setUpdateFormValues( recordValues ) {
        document.querySelector( '#idCategoryFields' ).value = recordValues.category_id
        document.querySelector( '#categoryFieldsUpdate' ).value = recordValues.category
        document.querySelector( '#activeStatusFields' ).checked = recordValues.active_status
        document.querySelector( '#activeStatusFields' ).value = recordValues.active_status
    }
}
class FormValidationImpl extends FormValidation {
    constructor() {
        super()
    }
    validateUpdateParams( updateParams ) {
        const validIdCategory = this.validateIdCategory( updateParams )
        const validCategory = this.validateCategory( updateParams )
        const validActiveStatus = this.validateActiveStatus( updateParams )

        if ( !validIdCategory ) return validIdCategory;
        if ( !validCategory ) return validCategory;
        if ( !validActiveStatus ) return validActiveStatus;
        return this.validateResult( 'Data is valid', true )
    }
    validateDeleteParams( deleteParams ) {
        if ( !deleteParams.category_id || deleteParams.category_id.length < 0 ) {
            return this.validateResult( 'Category Id doesnt found' )
        }
        return this.validateResult( 'Data is valid', true )
    }
    validateInsertParams( insertParams ) {
        return this.validateCategory( insertParams )
    }
    validateCategory( formData ) {
        if ( !formData.category ) {
            return this.validateResult( 'Cant insert empty category' )
        }
        if ( formData.category.length < 3 ) {
            return this.validateResult( 'Category too short' )
        }
        if ( formData.category.length > 200 ) {
            return this.validateResult( 'Category too long' )
        }
        return this.validateResult( 'Data is valid', true )
    }
    validateIdCategory( formData ) {
        if ( !formData.category_id || formData.category_id.length < 0 ) {
            return this.validateResult( 'Cant update  empty category' )
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
        const confirmMessage = `Are you sure to delete data ${ formValues.category_id } - ${ formValues.category } ?`
        document.getElementById( 'delete_confirm_massage_id' ).innerHTML = confirmMessage
        document.getElementById( 'delete_confirm_massage_id' ).value = formValues.category_id
    }
    clearAddNewDataForm() {
        document.querySelector( '#categoryFields' ).value = ''
    }
}

class ButtonEventImpl extends ButtonEvent {
    constructor() {
        super()
    }
    saveNewData() {
        const formAddNewValues = new FormDataImpl().getAddNewDataFormValues()
        const validationResult = new FormValidationImpl().validateInsertParams( formAddNewValues )
        if ( !validationResult.isValid ) {
            new Alert().showWarning( validationResult.message )
            new ModalFormImpl().enableFormButton( '#new_data_save_button_id' )
            return
        }
        new AjaxImpl().saveNewRecord( formAddNewValues )
    }
    saveUpdatedData() {
        const formUpdateValues = new FormDataImpl().getUpdateFormValues()
        const validationResult = new FormValidationImpl().validateUpdateParams( formUpdateValues )
        if ( !validationResult.isValid ) {
            new Alert().showWarning( validationResult.message )
            new ModalFormImpl().enableFormButton( '#button_save_updated_data_id' )
            return
        }
        new ModalFormImpl().disableFormButton( '#button_save_updated_data_id' )
        new AjaxImpl().updateData( formUpdateValues )
    }
    deleteData() {
        const deleteParams = new FormDataImpl().getDeleteFormValues()
        const validationResult = new FormValidationImpl().validateDeleteParams( deleteParams )
        if ( !validationResult.isValid ) {
            new Alert().showWarning( validationResult.message )
            new ModalForm().enableFormButton( '#button_delete_data_id' )
            return
        }
        new ModalFormImpl().disableFormButton( '#button_delete_data_id' )
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
                new DatatableCategoryProductImpl().reloadDatatable()
                return
            }
            new Alert().failedAjax( response.msg )
        }
        const ajaxCallback = {
            onSuccess: onSuccess,
            onFail: this.defaultOnFail,
            onFinal: () => {
                new ModalFormImpl().enableSaveConfirmBtn()
            }
        }
        this.sendAjax( { url: '/category_product_api', payload: payload }, ajaxCallback )
    }
    getSingleData( recordId ) {
        const payload = this.createPayload( 'POST', { 'category_id': recordId } )
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
            onFail: this.defaultOnFail,
            onFinal: this.defaultOnFinal
        }
        this.sendAjax( { url: '/category_product_api_search', payload: payload }, ajaxCallback )
    }
    getSingleDataForDeleteActions( recordId ) {
        const payload = this.createPayload( 'POST', { 'category_id': recordId } )
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
            onFail: this.defaultOnFail,
            onFinal: this.defaultOnFinal
        }
        this.sendAjax( { url: '/category_product_api_search', payload: payload }, ajaxCallback )
    }
    updateData( formData ) {
        console.log( 'ruunnn' )
        const payload = this.createPayload( 'PUT', formData )
        const onSuccess = ( response ) => {
            if ( !response.status ) {
                return new Alert().failedAjax( response.msg )
            }
            new Alert().successAjax( response.msg )
            new DatatableCategoryProductImpl().reloadDatatable()
            new ModalFormImpl().hideModal( 'id_modal_for_edit' )
            return
        }
        const ajaxCallback = {
            onSuccess: onSuccess,
            onFail: this.defaultOnFail,
            onFinal: () => {
                new ModalFormImpl().enableFormButton( '#button_save_updated_data_id' )
            }
        }
        this.sendAjax( { url: '/category_product_api', payload: payload }, ajaxCallback )
    }
    deleteData( formData ) {
        const payload = this.createPayload( 'DELETE', formData )
        const onSuccess = ( response ) => {
            if ( !response.status ) {
                return new Alert().failedAjax( response.msg )
            }
            new Alert().successAjax( response.msg )
            new DatatableCategoryProductImpl().reloadDatatable()
            new ModalFormImpl().hideModal( 'id_modal_for_delete' )
            return
        }
        const ajaxCallback = {
            onSuccess: onSuccess,
            onFail: this.defaultOnFail,
            onFinal: () => {
                new ModalFormImpl().enableFormButton( '#button_delete_data_id' )
            }
        }
        this.sendAjax( { url: '/category_product_api', payload: payload }, ajaxCallback )
    }
}

const runScript = () => {
    $( document ).ready( function () {
        const modalForm = new ModalFormImpl()
        new DatatableCategoryProductImpl().initiateDatatable()
        modalForm.registerOnHideModal()
        modalForm.disabledBtnNewDataOnClick()
        new ButtonEventImpl().bindEventWithAjax()
    } )
}

runScript()
