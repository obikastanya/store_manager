/** Class to save datatable config attributes, data class only. */
class DatatableAttributes {
    buttonEdit = `<button type="button" class="btn btn-warning btn-edit-company" 
                    onclick="new ModalForm().showModalCompany('id_modal_for_edit')" value="_data_">Edit</button>`
    buttonDelete = `<button type="button" class="btn btn-danger btn-delete-category-product" 
                    onclick="new ModalForm().showModalCategoryProduct('id_modal_for_delete')" value="_data_"
                    >Delete</button>`
    buttonCreateNewData = `<button type="button" class="btn btn-success" 
                            onclick="new ModalForm().showModalCompany('id_modal_for_add_new_data')" data="_data_"
                            >Add New Data</button>`
    tableColumns = [
        {
            data: null,
            defaultContent: ''
        },
        { data: 'company_id' },
        { data: 'company' },
        { data: 'active_status' },
        {
            data: null,
            render: ( data ) => {
                return this.buttonEdit.replace( "_data_", data.company_id ) + '&nbsp;' + this.buttonDelete.replace( "_data_", data.company_id )
            }
        }
    ]
    columnName = [
        { "name": "no", "targets": 0 },
        { "name": "category_id", "targets": 1 },
        { "name": "category", "targets": 2 },
        { "name": "active_status", "targets": 3 },
        { "name": "action", "targets": 4 }
    ]
    toolbarDomConfig = {
        // top for top toolbar, table for table position and bottom for (pagination and record showing info).
        top: `<'row'
            <'toolbar col col-sm-12 col-md-12 col-lg-6 justfiy-content-left text-left'>
            <'col col-sm-12 col-md-6 col-lg-6' 
            <'row'
            <'col col-sm-12 col-md-6'f>
            <'col col-sm-12 col-md-6'l>
            >>>`,
        table: "<'row'<'col-sm-12'tr>>",
        bottom: "<'row'<'col-sm-12 col-md-5'i><'col-sm-12 col-md-7'p>>"
    }
}

/** Class to manage datatable, set configuration, do ajax to retrieve data etc. */
class ApiForDatatableCompany extends DatatableAttributes {
    initiateDatatable() {
        let datatableCompany = $( '#category_product_datatable_id' ).DataTable( {
            ajax: {
                url: '/company_api',
                method: 'GET'
            },
            processing: true,
            serverSide: true,
            columns: this.tableColumns,
            columnDefs: this.columnName,
            order: [ [ 1, 'asc' ] ],
            dom: this.toolbarDomConfig.top + this.toolbarDomConfig.table + this.toolbarDomConfig.bottom,
            fnInitComplete: () => {
                //Set button create new data for toolbar
                $( 'div.toolbar' ).html( this.buttonCreateNewData )
            }
        } )
        new ModalButtonEvent().bindEventToDatatable( datatableCompany )
        this.addRowNumberToDatatable( datatableCompany )
    }
    reloadDatatable() {
        $( '#category_product_datatable_id' ).DataTable().ajax.reload()
    }

    addRowNumberToDatatable( datatable ) {
        datatable.on( 'draw.dt order.dt search.dt', function () {
            datatable.column( 0, { search: 'applied', order: 'applied' } ).nodes().each( function ( cell, i ) {
                cell.innerHTML = i + 1;
            } );
        } ).draw();
    }
}

/**Class to manage event in button inside modal pop up, its about final action such as save data, remove, etc */
class ModalButtonEvent {
    bindEvent() {
        const buttonSaveNewData = document.querySelector( '#new_data_save_button_id' )
        const buttonSaveChanges = document.querySelector( '#button_save_updated_data' )
        const buttonDeleteCategory = document.querySelector( '#button_delete_category' )
        buttonSaveNewData.addEventListener( 'click', this.saveCompany )
        buttonSaveChanges.addEventListener( 'click', this.saveUpdatedCompany )
        buttonDeleteCategory.addEventListener( 'click', this.deleteCategory )
    }
    saveCompany() {
        const formAddNewValues = new FormData().getAddNewDataFormValues()
        const validationResult = new FormValidation().validateCompany( formAddNewValues )
        if ( !validationResult.isValid ) {
            new Alert().showWarning( validationResult.message )
            new ModalForm().enableFormButton( '#new_data_save_button_id' )
            return
        }
        new Ajax().saveNewRecord( formAddNewValues )
    }
    saveUpdatedCompany() {
        const formUpdateValues = new FormData().getUpdateFormValues()
        const validationResult = new FormValidation().validateFormUpdateValues( formUpdateValues )
        if ( !validationResult.isValid ) {
            new Alert().showWarning( validationResult.message )
            new ModalForm().enableFormButton( '#button_save_updated_data' )
            return
        }
        new ModalForm().disableFormButton( '#button_save_updated_data' )
        new Ajax().updateCompany( formUpdateValues )
    }
    deleteCategory() {
        const deleteParameter = new FormData().getDeleteConfirmValues()
        const validationResult = new FormValidation().validateDeleteParameter( deleteParameter )
        if ( !validationResult.isValid ) {
            new Alert().showWarning( validationResult.message )
            new ModalForm().enableFormButton( '#button_delete_category' )
            return
        }
        new ModalForm().disableFormButton( '#button_delete_category' )
        new Ajax().deleteCategory( deleteParameter )

    }
    bindEventToDatatable( datatableCategoryProduct ) {
        datatableCategoryProduct.on( 'click', '.btn-edit-company', function ( e ) {
            new Ajax().getCompanyById( e.target.value )
        } )
        datatableCategoryProduct.on( 'click', '.btn-delete-category-product', function ( e ) {
            new Ajax().getCategoryByIdForDeleteActions( e.target.value )
        } )
    }
}

/**Class to manage event in modals likes showing modal, firing event when modal is hiding etc. */
class ModalForm {
    registerModalDefaultEvent() {
        const listIdModalForm = [ 'id_modal_for_add_new_data', 'id_modal_for_edit', 'id_modal_for_delete' ]
        for ( let idModal of listIdModalForm ) {
            // bind event into dom and spesific modal element, its only  work using jquery. 
            $( document ).on( 'hidden.bs.modal', '#' + idModal, () => {
                this.enableAllModalButton()
            } )
            if ( idModal == 'id_modal_for_add_new_data' ) {
                $( document ).on( 'hidden.bs.modal', '#' + idModal, () => {
                    this.setValueCompany( '' )
                } )
            }
        }
    }
    registerModalButtonEvent() {
        let eventCallbackSaveNewData = () => {
            this.disableFormButton( '#new_data_save_button_id' )
        }
        this.addEventToModalButton( '#new_data_save_button_id', eventCallbackSaveNewData )
    }

    enableAllModalButton() {
        this.enableFormButton( '#new_data_save_button_id' )
    }
    showModalCompany( idModal ) {
        // The modal wont show if we use pure javascript, the only way to make it work is using jquery.
        $( '#' + idModal ).modal( 'show' )
    }
    setDeleteConfirmMessage( formValues ) {
        const confirmMessage = `Apakah Anda yakin akan menghapus data ${ formValues.category_id } - ${ formValues.category } ?`
        document.getElementById( 'delete_confirm_massage_id' ).innerHTML = confirmMessage
        document.getElementById( 'delete_confirm_massage_id' ).value = formValues.category_id
    }
    hideModalCompany( idModal ) {
        // The modal wont hide if we use pure javascript, the only way to make it work is using jquery.
        $( '#' + idModal ).modal( 'hide' );
    }
    addEventToModalButton( buttonSelector, eventCallback ) {
        let button = document.querySelector( buttonSelector )
        button.addEventListener( 'click', eventCallback )
    }
    disableFormButton( buttonSelector ) {
        document.querySelector( buttonSelector ).setAttribute( 'disabled', '' )
    }
    enableFormButton( buttonSelector ) {
        document.querySelector( buttonSelector ).removeAttribute( 'disabled' )
    }
    setValueCompany( value ) {
        document.querySelector( '#companyFields' ).value = value
    }
    setFormUpdateValues( recordValues ) {
        document.querySelector( '#idCompanyFields' ).value = recordValues.company_id
        document.querySelector( '#companyFieldsUpdate' ).value = recordValues.company
        document.querySelector( '#activeStatusFields' ).checked = recordValues.active_status
        document.querySelector( '#activeStatusFields' ).value = recordValues.active_status
    }
}
/**Class to collecting data from a form . */
class FormData {
    getAddNewDataFormValues() {
        let formValues = {
            company: document.querySelector( '#companyFields' ).value
        }
        return formValues
    }
    getDeleteConfirmValues() {
        let formValues = {
            category_id: document.getElementById( 'delete_confirm_massage_id' ).value
        }
        return formValues
    }
    getActiveStatusValue( idFields ) {
        const isChecked = document.querySelector( idFields ).checked
        if ( isChecked ) return "Y";
        return "N"

    }
    getUpdateFormValues() {
        let formValues = {
            company: document.querySelector( '#companyFieldsUpdate' ).value,
            company_id: document.querySelector( '#idCompanyFields' ).value,
            active_status: this.getActiveStatusValue( '#activeStatusFields' )
        }
        return formValues
    }
}
/**Class to manage javascript request to back ends, doesnt including datatable ajax. */
class Ajax {
    createPayload( method, payloadBody ) {
        const payload = {
            method: method,
            headers: {
                'Content-type': 'application/json'
            },
            body: JSON.stringify( payloadBody )
        }
        return payload
    }
    saveNewRecord( formValues ) {
        const payload = this.createPayload( 'POST', formValues )
        const onSuccess = ( response ) => {
            if ( response.status ) {
                new ModalForm().hideModalCompany( 'id_modal_for_add_new_data' )
                new Alert().successAjax( response.msg )
                new ApiForDatatableCompany().reloadDatatable()
                return
            }
            new Alert().failedAjax( response.msg )
        }

        const onFail = ( error ) => {
            new Alert().error()
        }
        const onFinal = () => {
            new ModalForm().enableAllModalButton()
        }

        // In the first chain promise, we need to return response as response.json(), 
        // so the next chain will receive the data. Its because response.json() is also returning a promise.
        fetch( '/company_api', payload )
            .then( response => response.json() )
            .then( onSuccess )
            .catch( onFail )
            .finally( onFinal )
    }
    getCompanyById( companyId ) {
        const payload = this.createPayload( 'POST', { 'company_id': companyId } )
        const onSuccess = ( response ) => {
            console.log(response)
            if ( !response.data.length ) new Alert().failedAjax( response.msg );
            let recordValues = response.data[ 0 ]
            // the script bellow is a tenary operator, its update active_status to 1 if the current value is Y and 0 for others.
            recordValues.active_status = recordValues.active_status == 'Y' ? 1 : 0
            new ModalForm().setFormUpdateValues( recordValues )
            return
        }
        const onFail = ( error ) => {
            new Alert().error()
        }
        fetch( '/company_api_search', payload )
            .then( response => response.json() )
            .then( onSuccess )
            .catch( onFail )
    }
    getCategoryByIdForDeleteActions( categoryId ) {
        const payload = this.createPayload( 'POST', { 'category_id': categoryId } )
        const onSuccess = ( response ) => {
            if ( !response.data.length ) new Alert().failedAjax( response.msg );
            let recordValues = response.data[ 0 ]
            // the script bellow is a tenary operator, its update active_status to 1 if the current value is Y and 0 for others.
            recordValues.active_status = recordValues.active_status == 'Y' ? 1 : 0
            new ModalForm().setDeleteConfirmMessage( recordValues )
            return
        }
        const onFail = ( error ) => {
            new Alert().error()
        }
        fetch( '/category_product_api_search', payload )
            .then( response => response.json() )
            .then( onSuccess )
            .catch( onFail )
    }
    updateCompany( formData ) {
        const payload = this.createPayload( 'PUT', formData )
        const onSuccess = ( response ) => {
            if ( !response.status ) {
                return new Alert().failedAjax( response.msg )
            }
            new Alert().successAjax( response.msg )
            new ApiForDatatableCompany().reloadDatatable()
            new ModalForm().hideModalCompany( 'id_modal_for_edit' )
            return
        }
        const onFail = ( error ) => {
            new Alert().error()
        }
        const onFinal = () => {
            new ModalForm().enableFormButton( '#button_save_updated_data' )
        }
        fetch( '/company_api', payload )
            .then( response => response.json() )
            .then( onSuccess )
            .catch( onFail )
            .finally( onFinal )
    }
    deleteCategory( deleteParameter ) {
        const payload = this.createPayload( 'DELETE', deleteParameter )
        const onSuccess = ( response ) => {
            if ( !response.status ) {
                return new Alert().failedAjax( response.msg )
            }
            new Alert().successAjax( response.msg )
            new ApiForDatatableCompany().reloadDatatable()
            new ModalForm().hideModalCompany( 'id_modal_for_delete' )
            return
        }
        const onFail = ( error ) => {
            new Alert().error()
        }
        const onFinal = () => {
            new ModalForm().enableFormButton( '#button_delete_category' )
        }
        fetch( '/category_product_api', payload )
            .then( response => response.json() )
            .then( onSuccess )
            .catch( onFail )
            .finally( onFinal )
    }
}

/** Do validation to form values before sending request to back end */
class FormValidation {
    validateResult( message = '', isValid = false ) {
        return { isValid: isValid, message: message }
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
    validateFormUpdateValues( formData ) {
        const validIdCompany = this.validateIdCompany( formData )
        const validCompany = this.validateIdCompany( formData )
        const validActiveStatus = this.validateActiveStatus( formData )

        if ( !validIdCompany ) return validIdCompany;
        if ( !validCompany ) return validCompany;
        if ( !validActiveStatus ) return validActiveStatus;
        return this.validateResult( 'Data is valid', true )
    }
    validateDeleteParameter( deleteParameter ) {
        if ( !deleteParameter.category_id || deleteParameter.category_id.length < 0 ) {
            return this.validateResult( 'Category Id doesnt found' )
        }
        return this.validateResult( 'Data is valid', true )
    }
}

/** Run all script when document is ready. First initiate the datatatable, 
 * then attach event to button, modal, and all action button inside datatable. */
const runScript = () => {
    const api = new ApiForDatatableCompany()
    const modalForm = new ModalForm()
    const modalButtonEvent = new ModalButtonEvent()
    $( document ).ready( function () {
        api.initiateDatatable()
        // modalForm.registerModalButtonEvent()
        modalForm.registerModalDefaultEvent()
        modalButtonEvent.bindEvent()
    } )
}

runScript()
