class ButtonSelector {
    constructor() {
        this.saveNewRecord = '#new_data_save_button_id'
        this.btnSaveUpdatedRecord = '#button_save_updated_data_id'
        this.btnDeleteId = '#button_delete_data_id'
        this.btnClassEditData = '.btn-edit-data'
        this.btnClassDeleteData = '.btn-delete-data'
        this.modalEditId = 'id_modal_for_edit'
        this.modalDeleteId = 'id_modal_for_delete'
        this.modalAddNewRecordId = 'id_modal_for_add_new_data'
    }
}
class DatatableTools extends ButtonSelector {
    buttonEdit = `<button type="button" class="btn btn-warning btn-edit-data" 
                    onclick="new ModalForm().showModal('${ this.modalEditId }')"
                    value="_data_">Edit</button>`
    buttonDelete = `<button type="button" class="btn btn-danger btn-delete-data" 
                    onclick="new ModalForm().showModal('${ this.modalDeleteId }')" value="_data_"
                    >Delete</button>`
    buttonCreateNewData = `<button type="button" class="btn btn-success" 
                            onclick="new ModalForm().showModal('${ this.modalAddNewRecordId }')"
                            data="_data_"
                            >Add New Data</button>`
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
class BaseDatatable extends DatatableTools {
    constructor() {
        super()
        this.columnName = []
        this.tableColumns = []
        this.datatableId = ''
        this.apiEndpoint = '/'
    }
    getTableSetup() {
        const tableSetup = {
            ajax: {
                url: this.apiEndpoint,
                method: 'GET'
            },
            scrollX: true,
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
        }
        return tableSetup
    }

    initiateDatatable() {
        let datatableInstance = $( this.datatableId ).DataTable( this.getTableSetup() )
        this.bindEventForActionsButton( datatableInstance )
        this.addRowNumberToDatatable( datatableInstance )
    }
    reloadDatatable() {
        $( this.datatableId ).DataTable().ajax.reload()
    }
    addRowNumberToDatatable( datatable ) {
        datatable.on( 'draw.dt order.dt search.dt', function () {
            datatable.column( 0, { search: 'applied', order: 'applied' } ).nodes().each( function ( cell, i ) {
                cell.innerHTML = i + 1;
            } );
        } ).draw();
    }
    bindEventForActionsButton( datatableInstance ) { }
}


/**Class to manage event in button inside modal pop up, its about final action such as save data, remove, etc */
class ButtonEvent extends ButtonSelector {

    setMasterAsActiveMenu() {
        document.querySelector( '#master_side_link' ).classList.add( 'active' )
    }
    bindEventWithAjax() {
        const buttonSaveNewData = document.querySelector( this.saveNewRecord )
        const buttonSaveChanges = document.querySelector( this.btnSaveUpdatedRecord )
        const buttonDelete = document.querySelector( this.btnDeleteId )
        buttonSaveNewData.addEventListener( 'click', this.saveNewData )
        buttonSaveChanges.addEventListener( 'click', this.saveUpdatedData )
        buttonDelete.addEventListener( 'click', this.deleteData )
    }
    saveNewData() { }
    saveUpdatedData() { }
    deleteData() { }

}

/**Class to manage event in modals likes showing modal, firing event when modal is hiding etc. */
class ModalForm extends ButtonSelector {
    showModal( idModal ) {
        $( '#' + idModal ).modal( 'show' )
    }
    hideModal( idModal ) {
        $( '#' + idModal ).modal( 'hide' );
    }
    registerOnHideModal() {
        for ( let idModal of [ this.modalEditId, this.modalDeleteId, this.modalAddNewRecordId ] ) {
            $( document ).on( 'hidden.bs.modal', '#' + idModal, () => {
                // bind event into dom and spesific modal element, its only  work using jquery. 
                this.enableSaveConfirmBtn()
            } )
            if ( idModal == this.modalAddNewRecordId ) {
                $( document ).on( 'hidden.bs.modal', '#' + idModal, () => {
                    this.clearAddNewDataForm()
                } )
            }
        }
    }
    disabledBtnNewDataOnClick() {
        let eventCallbackSaveNewData = () => {
            this.disableFormButton( this.saveNewRecord )
        }
        let button = document.querySelector( this.saveNewRecord )
        button.addEventListener( 'click', eventCallbackSaveNewData )
    }
    enableSaveConfirmBtn() {
        this.enableFormButton( this.saveNewRecord )
    }
    disableFormButton( buttonSelector ) {
        document.querySelector( buttonSelector ).setAttribute( 'disabled', '' )
    }
    enableFormButton( buttonSelector ) {
        console.log( buttonSelector )
        document.querySelector( buttonSelector ).removeAttribute( 'disabled' )
    }
    setDeleteConfirmMessage( formValues ) { }
    clearAddNewDataForm() { }
}
/**Class to set or collecting data from a form . */
class FormData {
    getActiveStatusValue( idFields ) {
        const isChecked = document.querySelector( idFields ).checked
        if ( isChecked ) return "Y";
        return "N"
    }
    getAddNewDataFormValues() { }
    getDeleteFormValues() { }
    getUpdateFormValues() { }
    setUpdateFormValues( recordValues ) { }
}

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
    sendAjax( request, callback ) {
        fetch( request.url, request.payload )
            .then( response => response.json() )
            .then( callback.onSuccess )
            .catch( callback.onFail )
            .finally( callback.onFinal )
    }
    defaultOnFail( error ) {
        new Alert().error()
    }
    defaultOnFinal() { }
    saveNewRecord( formData ) { }
    getSingleData( recordId ) { }
    getSingleDataForDeleteActions( recordId ) { }
    updateData( formData ) { }
    deleteData( formData ) { }
}

/** Do validation to form values before sending request to back end */
class FormValidation {
    validateUpdateParams( updateParams ) { }
    validateDeleteParams( deleteParams ) { }
    validateInsertParams( insertParams ) { }
}