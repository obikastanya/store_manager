/** Class to save datatable config attributes, data class only. */
class DatatableAttributes {
    buttonEdit = `<button type="button" class="btn btn-warning btn-edit-category-product" 
                    onclick="new ModalForm().showModalCategoryProduct('id_modal_for_edit')" value="_data_">Edit</button>`
    buttonDelete = `<button type="button" class="btn btn-danger btn-delete-category-product" 
                    onclick="new ModalForm().showModalCategoryProduct('id_modal_for_delete')" value="_data_"
                    >Delete</button>`
    buttonCreateNewData = `<button type="button" class="btn btn-success" 
                            onclick="new ModalForm().showModalCategoryProduct('id_modal_for_add_new_data')" data="_data_"
                            >Add New Data</button>`
    tableColumns = [
        {
            data: null,
            defaultContent: ''
        },
        { data: 'category_id' },
        { data: 'category' },
        { data: 'active_status' },
        {
            data: null,
            render: ( data ) => {
                return this.buttonEdit.replace( "_data_", data.category_id ) + '&nbsp;' + this.buttonDelete.replace( "_data_", data.category_id )
            }
        }
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
class ApiForDatatableCategoryProduct extends DatatableAttributes {
    initiateDatatable() {
        let datatableCategoryProduct = $( '#category_product_datatable_id' ).DataTable( {
            ajax: {
                url: '/category_product_api',
                method: 'GET'
            },
            columns: this.tableColumns,
            order: [ [ 1, 'asc' ] ],
            dom: this.toolbarDomConfig.top + this.toolbarDomConfig.table + this.toolbarDomConfig.bottom,
            fnInitComplete: () => {
                //Set button create new data for toolbar
                $( 'div.toolbar' ).html( this.buttonCreateNewData )
            }
        } )
        new ModalButtonEvent().bindEventToDatatable( datatableCategoryProduct )
        this.addRowNumberToDatatable( datatableCategoryProduct )
    }
    reloadDatatable() {
        $( '#category_product_datatable_id' ).DataTable().ajax.reload()
    }

    addRowNumberToDatatable( datatable ) {
        datatable.on( 'order.dt search.dt', function () {
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
        buttonSaveNewData.addEventListener( 'click', this.saveCategoryProduct )
        buttonSaveChanges.addEventListener( 'click', this.saveUpdatedCategoryProduct )
    }
    saveCategoryProduct() {
        const formAddNewValues = new FormData().getAddNewDataFormValues()
        const validationResult = new FormValidation().validateCategory( formAddNewValues )
        if ( !validationResult.isValid ) {
            new Alert().showWarning( validationResult.message )
            new ModalForm().enableFormButton( '#new_data_save_button_id' )
            return
        }
        new Ajax().saveNewRecord( formAddNewValues )
    }
    saveUpdatedCategoryProduct() {
        const formUpdateValues = new FormData().getUpdateFormValues()
        const validationResult = new FormValidation().validateFormUpdateValues( formUpdateValues )
        if ( !validationResult.isValid ) {
            new Alert().showWarning( validationResult.message )
            new ModalForm().enableFormButton( '#button_save_updated_data' )
            return
        }
        new ModalForm().disableFormButton( '#button_save_updated_data' )
        new Ajax().updateCategory( formUpdateValues )
    }
    bindEventToDatatable( datatableCategoryProduct ) {
        datatableCategoryProduct.on( 'click', '.btn-edit-category-product', function ( e ) {
            new Ajax().getCategoryById( e.target.value )
        } )
        datatableCategoryProduct.on( 'click', '.btn-delete-category-product', function ( e ) {
            new ModalButtonEvent().showFormDeleteCategoryProduct()
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
                    this.setValueCategory( '' )
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
    showModalCategoryProduct( idModal ) {
        // The modal wont show if we use pure javascript, the only way to make it work is using jquery.
        $( '#' + idModal ).modal( 'show' )
    }
    hideModalCategoryProduct( idModal ) {
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
    setValueCategory( value ) {
        document.querySelector( '#categoryFields' ).value = value
    }
    setFormUpdateValues( recordValues ) {
        document.querySelector( '#idCategoryFields' ).value = recordValues.category_id
        document.querySelector( '#categoryFields' ).value = recordValues.category
        document.querySelector( '#activeStatusFields' ).checked = recordValues.active_status
        document.querySelector( '#activeStatusFields' ).value = recordValues.active_status
    }
}
/**Class to collecting data from a form . */
class FormData {
    getAddNewDataFormValues() {
        let formValues = {
            category: document.querySelector( '#categoryFields' ).value
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
            category: document.querySelector( '#categoryFields' ).value,
            category_id: document.querySelector( '#idCategoryFields' ).value,
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
            new ModalForm().enableAllModalButton()
            if ( response.status ) {
                new ModalForm().hideModalCategoryProduct( 'id_modal_for_edit' )
                new Alert().successAjax( response.msg )
                new ApiForDatatableCategoryProduct().reloadDatatable()
                return
            }
            new Alert().failedAjax( response.msg )
        }

        const onFail = ( error ) => {
            new Alert().error()
        }

        // In the first chain promise, we need to return response as response.json(), 
        // so the next chain will receive the data. Its because response.json() is also returning a promise.
        fetch( '/category_product_api', payload )
            .then( response => response.json() )
            .then( onSuccess )
            .catch( onFail )
    }
    getCategoryById( categoryId ) {
        const payload = this.createPayload( 'POST', { 'category_id': categoryId } )
        const onSuccess = ( response ) => {
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
        fetch( '/category_product_api_search', payload )
            .then( response => response.json() )
            .then( onSuccess )
            .catch( onFail )
    }
    updateCategory( formData ) {
        const payload = this.createPayload( 'PUT', formData )
        const onSuccess = ( response ) => {
            if ( !response.status ) {
                return new Alert().failedAjax( response.msg )
            }
            new Alert().successAjax( response.msg )
            new ApiForDatatableCategoryProduct().reloadDatatable()
            new ModalForm().hideModalCategoryProduct
            return
        }
        const onFail = ( error ) => {
            new Alert().error()
        }
        const onFinal = () => {
            new ModalForm().enableFormButton( '#button_save_updated_data' )
        }
        fetch( '/category_product_api', payload )
            .then( response => response.json() )
            .then( onSuccess )
            .catch( onFail )
            .finally( onFinal )
    }

}

/** Class to handle Pop Up thats shown whenever an action is done */
class Alert {
    showAlert( message, messageIcon = 'error' ) {
        swal( {
            text: message,
            icon: messageIcon
        } )
    }
    error() {
        this.showAlert( 'Something wrong while trying to complete the request' )
    }
    successAjax( message ) {
        this.showAlert( message, 'success' )
    }
    failedAjax( message ) {
        this.showAlert( message )
    }
    showWarning( message ) {
        this.showAlert( message, 'warning' )
    }
}
/** Do validation to form values before sending request to back end */
class FormValidation {
    validateResult( message = '', isValid = false ) {
        return { isValid: isValid, message: message }
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
            return this.validateResult( 'Category update  empty category' )
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
        const validIdCategory = this.validateIdCategory( formData )
        const validCategory = this.validateIdCategory( formData )
        const validActiveStatus = this.validateActiveStatus( formData )

        if ( !validIdCategory ) return validIdCategory;
        if ( !validCategory ) return validCategory;
        if ( !validActiveStatus ) return validActiveStatus;
        return this.validateResult( 'Data is valid', true )
    }
}

/** Run all script when document is ready. First initiate the datatatable, 
 * then attach event to button, modal, and all action button inside datatable. */
const runScript = () => {
    const api = new ApiForDatatableCategoryProduct()
    const modalForm = new ModalForm()
    const modalButtonEvent = new ModalButtonEvent()
    $( document ).ready( function () {
        api.initiateDatatable()
        modalForm.registerModalButtonEvent()
        modalForm.registerModalDefaultEvent()
        modalButtonEvent.bindEvent()
    } )
}

runScript()
