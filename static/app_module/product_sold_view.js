class DatatableProductSoldImpl extends BaseDatatable {
    constructor() {
        super()
        this.tableColumns = [
            {
                data: null,
                defaultContent: ''
            },
            {
                data: 'transaction_id'
            },
            {
                data: 'transaction_date'
            },
            {
                data: 'employee_transaction',
                render: ( data ) => {
                    return data.name

                }
            },
            {
                data: 'payment_method',
                render: ( data ) => {
                    return data.payment_method

                }
            },
            {
                data: 'total_price'
            },
            {
                data: 'tax'
            },
            {
                data: 'paid'
            },
            {
                data: 'change'
            },
            {
                data: null,
                render: ( data ) => {
                    const buttonDetail = `<button type="button" class="btn btn-warning btn-detail-data" value=${ data.transaction_id } onclick="new ModalForm().showModal('id_modal_for_detail_data')">Detail</button>`
                    return buttonDetail + '&nbsp;' + this.buttonDelete.replace( "_data_", data.transaction_id )
                }
            }
        ]
        this.columnName = [
            { "name": "no", "targets": 0 },
            { "name": "transaction_id", "targets": 1 },
            { "name": "transaction_date", "targets": 2 },
            { "name": "cashier", "targets": 3 },
            { "name": "payment_method", "targets": 4 },
            { "name": "total_price", "targets": 5 },
            { "name": "tax", "targets": 6 },
            { "name": "paid", "targets": 7 },
            { "name": "change", "targets": 8 },
            { "name": "action", "targets": 9 }
        ]
        this.datatableId = '#product_sold_transaction_datatable_id'
        this.apiEndpoint = '/product_sold_api'
    }
    getTableSetup() {
        const getDataFromFields = ( id ) => {
            try {
                const value = document.querySelector( id ).value
                return value
            }
            catch ( e ) {
                return null
            }
        }
        const tableSetup = {
            ajax: {
                url: this.apiEndpoint,
                method: 'GET',
                data: ( data ) => {
                    console.log( getDataFromFields( '#productFields' ) )
                    data.product_id = getDataFromFields( '#productFields' )
                    data.discount_id = getDataFromFields( '#discountFields' )
                    data.cashier_id = getDataFromFields( '#cashierFields' )
                    data.transaction_date = getDataFromFields( '#transactionDateFields' )
                }
            },
            language: {
                searchPlaceholder: "Search transaction code"
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
        }
        return tableSetup
    }
    bindEventForActionsButton( datatableInstance ) {
        datatableInstance.on( 'click', '.btn-detail-data', function ( e ) {
            new AjaxImpl().getSingleData( e.target.value )
        } )
        datatableInstance.on( 'click', this.btnClassDeleteData, ( e ) => {
            // new AjaxImpl().getSingleDataForDeleteActions( e.target.value )
            new ModalFormImpl().setDeleteConfirmMessage( e.target.value )
        } )
    }
}

class FormDataImpl extends FormData {
    constructor() {
        super()
    }
    getAddNewDataFormValues() {
        let formValues = {
            product_id: document.querySelector( '#productIdFields' ).value,
            discount_id: document.querySelector( '#discountIdFields' ).value,
            start_date: document.querySelector( '#startDateFields' ).value,
            expired_date: document.querySelector( '#expiredDateFields' ).value
        }
        return formValues
    }
    getDeleteFormValues() {
        let formValues = {
            transaction_id: document.getElementById( 'delete_confirm_massage_id' ).value
        }
        return formValues
    }
    getUpdateFormValues() {
        let formValues = {
            product_id: document.querySelector( '#productIdUpdateFields' ).value,
            discount_id: document.querySelector( '#discountIdUpdateFields' ).value,
            start_date: document.querySelector( '#startDateUpdateFields' ).value,
            expired_date: document.querySelector( '#expiredDateUpdateFields' ).value,
            active_status: this.getActiveStatusValue( '#activeStatusFields' )
        }
        return formValues
    }
    setUpdateFormValues( recordValues ) {
        document.querySelector( '#productIdUpdateFields' ).value = recordValues.discount_product.product_id
        document.querySelector( '#discountIdUpdateFields' ).value = recordValues.discount_master.discount_id
        document.querySelector( '#startDateUpdateFields' ).value = recordValues.start_date
        document.querySelector( '#expiredDateUpdateFields' ).value = recordValues.expired_date
        document.querySelector( '#activeStatusFields' ).checked = recordValues.active_status
        document.querySelector( '#activeStatusFields' ).value = recordValues.active_status
    }
    generateRow( record ) {
        const replaceEmpty = ( value ) => {
            if ( value ) return value
            if ( value === 0 ) return value;
            return '-';

        }
        let rowRecord = `<tr>
                            <td>${ replaceEmpty( record.index + 1 ) }</td>
                            <td>${ replaceEmpty( record.product.product_id ) }</td>
                            <td>${ replaceEmpty( record.product.product_desc ) }</td>
                            <td>${ replaceEmpty( record.quantity ) }</td>
                            <td>${ replaceEmpty( record.saled_price ) }</td>
                            <td>${ replaceEmpty( record.quantity * record.saled_price ) }</td>
                            <td>${ replaceEmpty( this.getCuttOff( record.detail_discount_applied ) ) }</td>
                            <td>${ replaceEmpty( this.getDiscountNames( record.detail_discount_applied ) ) }</td>
                        </tr>`
        return rowRecord
    }

    setDetailModalTables( recordValues ) {
        let tableContent = ""
        for ( let [ index, record ] of recordValues.entries() ) {
            record.index = index
            tableContent += this.generateRow( record )
        }
        let table = document.querySelector( '#product_sold_detail_transaction_datatable_id > tbody' )
        table.innerHTML = tableContent
    }
    generateOption( recordValues ) {
        let options = ''
        for ( const values of recordValues ) {
            options += ` <option value=${ values.id }>${ values.description }</option> `
        }
        return options
    }
    setOptionForSelectFields( elementsToSet, recordValues ) {
        // some dom manipulation
        for ( const id of elementsToSet ) {
            const options = this.generateOption( recordValues )
            document.querySelector( id ).innerHTML = ''
            document.querySelector( id ).innerHTML = options
        }
    }
    getCuttOff( discountApplied ) {
        let cuttOff = 0
        for ( const discount of discountApplied ) {
            cuttOff += discount.cutt_off_nominal
        }
        return cuttOff
    }
    getDiscountNames( discountApplied ) {
        let discountNames = []
        for ( const discount of discountApplied ) {
            discountNames.push( discount.discount_applied.discount_master.desc )
        }
        return discountNames.join( ", " )
    }
}
class FormValidationImpl extends FormValidation {
    constructor() {
        super()
    }
    validateUpdateParams( updateParams ) {
        const validIdProduct = this.validateIdProduct( updateParams )
        const validIdDiscount = this.validateIdDiscount( updateParams )
        const validStartDate = this.validateStartDate( updateParams )
        const validExpiredDate = this.validateExpiredDate( updateParams )
        const validActiveStatus = this.validateActiveStatus( updateParams )

        if ( !validIdProduct.isValid ) return validIdProduct;
        if ( !validIdDiscount.isValid ) return validIdDiscount;
        if ( !validStartDate.isValid ) return validStartDate;
        if ( !validExpiredDate.isValid ) return validExpiredDate;
        if ( !validActiveStatus.isValid ) return validActiveStatus;
        return this.validateResult( 'Data is valid', true )
    }
    validateDeleteParams( deleteParams ) {
        const validTransactionId = this.validateTransactionId( deleteParams )
        if ( !validTransactionId.isValid ) return validTransactionId;
        return this.validateResult( 'Data is valid', true )
    }
    validateInsertParams( insertParams ) {
        const validIdProduct = this.validateIdProduct( insertParams )
        const validIdDiscount = this.validateIdDiscount( insertParams )
        const validStartDate = this.validateStartDate( insertParams )
        const validExpiredDate = this.validateExpiredDate( insertParams )

        if ( !validIdProduct.isValid ) return validIdProduct;
        if ( !validIdDiscount.isValid ) return validIdDiscount;
        if ( !validStartDate.isValid ) return validStartDate;
        if ( !validExpiredDate.isValid ) return validExpiredDate;
        return this.validateResult( 'Data is valid', true )
    }
    validateTransactionId( formData ) {
        if ( isNaN( formData.transaction_id ) ) {
            return this.validateResult( 'Invalid transaction selected' )
        }
        if ( !( parseInt( formData.transaction_id ) ) ) {
            return this.validateResult( 'Invalid transaction selected' )
        }
        return this.validateResult( 'Data is valid', true )
    }
    validateIdDiscount( formData ) {
        if ( isNaN( formData.discount_id ) ) {
            return this.validateResult( 'Invalid master discount selected' )
        }
        if ( !( parseInt( formData.product_id ) ) ) {
            return this.validateResult( 'Invalid Product selected' )
        }
        return this.validateResult( 'Data is valid', true )
    }
    validateStartDate( formData ) {
        if ( !formData.start_date ) {
            return this.validateResult( 'Start date is empty' )
        }
        return this.validateResult( 'Data is valid', true )
    }
    validateExpiredDate( formData ) {
        if ( !formData.expired_date ) {
            return this.validateResult( 'Expired date is empty' )
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
    createSelectFields() {
        $( '.selectForm' ).selectize( {
            sortField: 'text',
            create: false
        } );
    }
    bindEventToFormFilter() {
        const btnFilterData = document.querySelector( '.btn-filter-product-sold' )
        btnFilterData.addEventListener( 'click', () => {
            new DatatableProductSoldImpl().reloadDatatable()
        } )
    }
    setDeleteConfirmMessage( recordId ) {
        const confirmMessage = `Area you sure to delete transaction with id ${ recordId } ?`
        document.getElementById( 'delete_confirm_massage_id' ).innerHTML = confirmMessage
        document.getElementById( 'delete_confirm_massage_id' ).value = recordId
    }
    clearFormFilter() {
        document.querySelector( '#productFields' ).value = ''
        document.querySelector( '#discountFields' ).value = ''
        document.querySelector( '#cashierFields' ).value = ''

    }
    clearAddNewDataForm() {
        document.querySelector( '#productIdFields' ).value = ''
        document.querySelector( '#discountIdFields' ).value = ''
        document.querySelector( '#startDateFields' ).value = ''
        document.querySelector( '#expiredDateFields' ).value = ''
    }
}

class ButtonEventImpl extends ButtonEvent {
    constructor() {
        super()
    }
    bindEventWithAjax() {
        // const buttonSaveNewData = document.querySelector( this.saveNewRecord )
        // const buttonSaveChanges = document.querySelector( this.btnSaveUpdatedRecord )
        // buttonSaveNewData.addEventListener( 'click', this.saveNewData )
        // buttonSaveChanges.addEventListener( 'click', this.saveUpdatedData )
        const buttonDelete = document.querySelector( this.btnDeleteId )
        buttonDelete.addEventListener( 'click', this.deleteData )
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
                new DatatableProductSoldImpl().reloadDatatable()
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
        this.sendAjax( { url: '/manage_discount_api', payload: payload }, ajaxCallback )
    }
    getSingleData( recordId ) {
        const params = {
            transaction_id: recordId
        }
        const payload = this.createPayload( 'POST', params )
        const onSuccess = ( response ) => {
            if ( !response.data.length ) new Alert().failedAjax( response.msg );
            new FormDataImpl().setDetailModalTables( response.data[ 0 ].detail_transaction )
            return
        }
        const ajaxCallback = {
            onSuccess: onSuccess,
            onFail: ( error ) => {
                console.log( error )
                new Alert().error()
            },
            onFinal: () => { }
        }
        this.sendAjax( { url: '/product_sold_api_search', payload: payload }, ajaxCallback )
    }
    // getSingleDataForDeleteActions( recordId ) {
    //     const params = {
    //         product_id: recordId.split( ',' )[ 0 ],
    //         discount_id: recordId.split( ',' )[ 1 ]
    //     }
    //     const payload = this.createPayload( 'POST', params )
    //     const onSuccess = ( response ) => {
    //         if ( !response.data.length ) new Alert().failedAjax( response.msg );
    //         let recordValues = response.data[ 0 ]
    //         // the script bellow is a tenary operator, its update active_status to 1 if the current value is Y and 0 for others.
    //         recordValues.active_status = recordValues.active_status == 'Y' ? 1 : 0
    //         new ModalFormImpl().setDeleteConfirmMessage( recordValues )
    //         return
    //     }
    //     const ajaxCallback = {
    //         onSuccess: onSuccess,
    //         onFail: ( error ) => {
    //             new Alert().error()
    //         },
    //         onFinal: () => { }
    //     }
    //     this.sendAjax( { url: '/manage_discount_api_search', payload: payload }, ajaxCallback )

    // }
    updateData( formData ) {
        const payload = this.createPayload( 'PUT', formData )
        const onSuccess = ( response ) => {
            if ( !response.status ) {
                return new Alert().failedAjax( response.msg )
            }
            new Alert().successAjax( response.msg )
            new DatatableProductSoldImpl().reloadDatatable()
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
        this.sendAjax( { url: '/manage_discount_api', payload: payload }, ajaxCallback )

    }
    deleteData( formData ) {
        const payload = this.createPayload( 'DELETE', formData )
        const onSuccess = ( response ) => {
            if ( !response.status ) {
                return new Alert().failedAjax( response.msg )
            }
            new Alert().successAjax( response.msg )
            new DatatableProductSoldImpl().reloadDatatable()
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

        this.sendAjax( { url: '/product_sold_api', payload: payload }, ajaxCallback )
    }
    getOption( endPoint, onSuccess = () => { } ) {
        return fetch( endPoint )
            .then( response => response.json() )
            .then( onSuccess )
            .catch( ( err ) => { console.log( err ) } ).finally( () => {
                return Promise.resolve( 1 )
            } )
    }
    getLovForProductFields() {
        const extractIdDescriptionFunc = ( recordValues ) => {
            let newRecordValues = []
            for ( const record of recordValues ) {
                newRecordValues.push( { id: record.product_id, description: record.product_desc } )
            }
            return newRecordValues
        }
        const onSuccess = ( response ) => {
            let newRecordValues = extractIdDescriptionFunc( response.data )
            const selectFieldIds = [ '#productFields' ]
            new FormDataImpl().setOptionForSelectFields( selectFieldIds, newRecordValues )
        }
        return this.getOption( '/product_lov_api', onSuccess )
    }
    getLovForDiscountFields() {
        const extractIdDescriptionFunc = ( recordValues ) => {
            let newRecordValues = []
            for ( const record of recordValues ) {
                newRecordValues.push( { id: record.discount_id, description: record.desc } )
            }
            return newRecordValues
        }
        const onSuccess = ( response ) => {
            let newRecordValues = extractIdDescriptionFunc( response.data )
            const selectFieldIds = [ '#discountFields' ]
            new FormDataImpl().setOptionForSelectFields( selectFieldIds, newRecordValues )
        }
        return this.getOption( '/discount_lov_api', onSuccess )
    }
    getLovForEmployeeFields() {
        const extractIdDescriptionFunc = ( recordValues ) => {
            let newRecordValues = []
            for ( const record of recordValues ) {
                newRecordValues.push( { id: record.employee_id, description: record.name } )
            }
            return newRecordValues
        }
        const onSuccess = ( response ) => {
            let newRecordValues = extractIdDescriptionFunc( response.data )
            const selectFieldIds = [ '#cashierFields' ]
            new FormDataImpl().setOptionForSelectFields( selectFieldIds, newRecordValues )
        }
        return this.getOption( '/employee_lov_api', onSuccess )
    }
    getLovForSelectField() {
        const callLovAjax = async () => {
            const promiseList = [ this.getLovForProductFields(), this.getLovForDiscountFields(), this.getLovForEmployeeFields() ]
            await Promise.all( promiseList ).then( () => {
                new ModalFormImpl().clearFormFilter()
                new ModalFormImpl().createSelectFields()
            } )
        }
        callLovAjax()
    }
}

const runScript = () => {
    $( document ).ready( function () {
        const modalForm = new ModalFormImpl()
        new DatatableProductSoldImpl().initiateDatatable()
        new AjaxImpl().getLovForSelectField()
        modalForm.bindEventToFormFilter()
        // modalForm.registerOnHideModal()
        // modalForm.disabledBtnNewDataOnClick()
        new ButtonEventImpl().bindEventWithAjax()
    } )
}

runScript()
