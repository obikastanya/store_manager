$( document ).ready( function () {
    new AjaxAction().getLovForSelectField()
    new ReportView().addEventListenerToBtnExport()
    new ReportView().setAsActiveMenu()
} )

class ReportView {
    addEventListenerToBtnExport() {
        const buttonExport = document.querySelector( '.btn-export' )
        buttonExport.addEventListener( 'click', this.exportData )
    }
    setAsActiveMenu() {
        document.querySelector( '#report_side_link' ).classList.add( 'active' )
    }
    exportData() {
        let transactionFilter = new ReportView().getDataFromAForm()
        if ( transactionFilter.transaction_type == "purchased_product" ) {
            return new AjaxAction().exportPurchasedProduct( transactionFilter )
        }
        if ( transactionFilter.transaction_type == "sold_product" ) {
            return new AjaxAction().exportSoldProduct( transactionFilter )
        }
        return new Alert().showWarning( "Transaction is not selected" )

    }
    getDataFromAForm() {
        const getValue = ( idElement ) => document.querySelector( idElement ).value;
        const transactionFilter = {
            date_month: this.parseToInt( getValue( '#monthField' ) ),
            date_year: this.parseToInt( getValue( '#yearField' ) ),
            product_id: this.parseToInt( getValue( '#productField' ) ),
            category_id: this.parseToInt( getValue( '#categoryProductField' ) ),
            transaction_type: this.parseToInt( getValue( '#transactionTypeField' ) )
        }
        return transactionFilter
    }
    parseToInt( value ) {
        if ( !value ) return value;
        if ( isNaN( value ) ) return value;
        return parseInt( value )
    }
    downloadExcelSilently( blobExcelFile, filename ) {
        const url = window.URL.createObjectURL( blobExcelFile );
        const hiddenAnchor = document.createElement( "a" );
        hiddenAnchor.style.display = "none";
        hiddenAnchor.href = url;
        hiddenAnchor.download = filename;
        document.body.appendChild( hiddenAnchor );
        hiddenAnchor.click();
        window.URL.revokeObjectURL( url );
    }
    clearFormFilter() {
        document.querySelector( '#categoryProductField' ).value = ''
        document.querySelector( '#productField' ).value = ''
    }
    setOptionForSelectFields( elementsToSet, recordValues ) {
        for ( const id of elementsToSet ) {
            const options = this.generateOption( recordValues )
            document.querySelector( id ).innerHTML = ''
            document.querySelector( id ).innerHTML = options
        }
    }
    generateOption( recordValues ) {
        let options = ''
        for ( const values of recordValues ) {
            options += ` <option value=${ values.id }>${ values.description }</option> `
        }
        return options
    }
    createSelectFields() {
        $( '.selectForm' ).selectize( {
            sortField: 'text',
            create: false
        } );
    }

}

class AjaxAction {
    exportSoldProduct( transactionFilter ) {
        let payload = this.createPayload( transactionFilter )
        const onSuccessCallback = ( resp ) => {
            if ( !resp.status ) {
                new Alert().showAlert( resp.msg )
                return
            }

            const convertedExcelToBuffer = base64DecToArr( resp.data ).buffer;
            const excelInBlob = new Blob( [ convertedExcelToBuffer ] )
            const currentTime = new Date()
            const generatedTime = `${ currentTime.getDate() }/${ currentTime.getMonth() + 1 }/${ currentTime.getFullYear() } ${ currentTime.getHours() }:${ currentTime.getMinutes() }`
            const fileName = 'transaction_sold_report_generate_on_' + generatedTime
            new ReportView().downloadExcelSilently( excelInBlob, fileName + '.xlsx' )
        }

        fetch( '/report_transaction_sold', payload )
            .then( response => response.json() )
            .then( onSuccessCallback )
            .catch( ( err ) => { console.log( err ) } )
    }
    exportPurchasedProduct( transactionFilter ) {
        let payload = this.createPayload( transactionFilter )
        const onSuccessCallback = ( resp ) => {
            if ( !resp.status ) {
                new Alert().showAlert( resp.msg )
                return
            }

            const convertedExcelToBuffer = base64DecToArr( resp.data ).buffer;
            const excelInBlob = new Blob( [ convertedExcelToBuffer ] )
            const currentTime = new Date()
            const generatedTime = `${ currentTime.getDate() }/${ currentTime.getMonth() + 1 }/${ currentTime.getFullYear() } ${ currentTime.getHours() }:${ currentTime.getMinutes() }`
            const fileName = 'transaction_purchased_report_generate_on_' + generatedTime
            new ReportView().downloadExcelSilently( excelInBlob, fileName + '.xlsx' )
        }

        fetch( '/report_transaction_purchased', payload )
            .then( response => response.json() )
            .then( onSuccessCallback )
            .catch( ( err ) => { console.log( err ) } )
    }
    getLovForSelectField() {
        const callLovAjax = async () => {
            const promiseList = [ this.getLovForProductFields(), this.getLovForCategoryFields() ]
            await Promise.all( promiseList ).then( () => {
                new ReportView().clearFormFilter()
                new ReportView().createSelectFields()
            } )
        }
        callLovAjax()
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
            const selectFieldIds = [ '#productField' ]
            new ReportView().setOptionForSelectFields( selectFieldIds, newRecordValues )
        }
        return this.getOption( '/product_lov_api', onSuccess )
    }
    getLovForCategoryFields() {
        const extractIdDescriptionFunc = ( recordValues ) => {
            let newRecordValues = []
            for ( const record of recordValues ) {
                newRecordValues.push( { id: record.category_id, description: record.category } )
            }
            return newRecordValues
        }
        const onSuccess = ( response ) => {
            let newRecordValues = extractIdDescriptionFunc( response.data )
            const selectFieldIds = [ '#categoryProductField' ]
            new ReportView().setOptionForSelectFields( selectFieldIds, newRecordValues )
        }
        this.getOption( '/category_product_lov_api', onSuccess )

    }
    getOption( endPoint, onSuccess = () => { } ) {
        return fetch( endPoint )
            .then( response => response.json() )
            .then( onSuccess )
            .catch( ( err ) => { console.log( err ) } ).finally( () => {
                return Promise.resolve( 1 )
            } )
    }

    createPayload( payloadBody ) {
        const payload = {
            method: "POST",
            headers: {
                'Content-type': 'application/json'
            },
            body: JSON.stringify( payloadBody )
        }
        return payload
    }

}
