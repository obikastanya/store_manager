class DatatableAttributes {
    buttonEdit = `<button type="button" class="btn btn-warning btn-edit-category-product" 
                    onclick="new ModalForm().showModalCategoryProduct('id_modal_for_edit')">Edit</button>`
    buttonDelete = `<button type="button" class="btn btn-danger " 
                    onclick="new ModalForm().showModalCategoryProduct('id_modal_for_delete')"
                    >Delete</button>`
    buttonCreateNewData = `<button type="button" class="btn btn-success" 
                            onclick="new ModalForm().showModalCategoryProduct('id_modal_for_add_new_data')"
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
            defaultContent: this.buttonEdit + '&nbsp;' + this.buttonDelete
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
        this.addRowNumberToDatatable( datatableCategoryProduct )
    }

    addRowNumberToDatatable( datatable ) {
        datatable.on( 'order.dt search.dt', function () {
            datatable.column( 0, { search: 'applied', order: 'applied' } ).nodes().each( function ( cell, i ) {
                cell.innerHTML = i + 1;
            } );
        } ).draw();
    }
}

class ModalButtonEvent {
    bindEvent() {
        const buttonSaveNewData = document.querySelector( '#new_data_save_button_id' )
        buttonSaveNewData.addEventListener( 'click', this.saveCategoryProduct )
    }
    saveCategoryProduct() {
        const formAddNewValues = new FormData().getAddNewDataFormValues()
        new Ajax().sendRequestToSaveNewRecord( formAddNewValues )
    }
}

class ModalForm {
    registerModalDefaultEvent() {
        const listIdModalForm = [ 'id_modal_for_add_new_data', 'id_modal_for_edit', 'id_modal_for_delete' ]
        for ( let idModal of listIdModalForm ) {
            // bind event into dom and spesific modal element, its only  work using jquery. 
            $( document ).on( 'hidden.bs.modal', '#' + idModal, () => {
                this.enableAllModalButton()
            } )
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
        var modal = new bootstrap.Modal( document.getElementById( idModal ) )
        modal.show()
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
}
class FormData {
    getAddNewDataFormValues() {
        let formValues = {
            category: document.querySelector( '#categoryFields' ).value
        }
        return formValues
    }
}
class Ajax {
    sendRequestToSaveNewRecord( formValues ) {
        const payload = {
            method: 'POST',
            headers: {
                'Content-type': 'application/json'
            },
            body: JSON.stringify( formValues )
        }
        const onSuccess = ( response ) => {
            alert( response.msg )
        }
        const onFail = ( error ) => {
            console.log( error )
        }

        // In the first chain promise, we need to return response as response.json(), 
        // so the next chain will receive the data. Its because response.json() is also returning a promise.
        fetch( '/category_product_api', payload )
            .then( response => response.json() )
            .then( onSuccess )
            .catch( onFail )
    }

}
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