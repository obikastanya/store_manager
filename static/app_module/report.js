$( document ).ready( function () {
    new AjaxAction().getLovForSelectField()

} )

class ReportView {
    downloadExcelSilently( blobExcelFile, filename ) {
        const url = window.URL.createObjectURL( blobExcelFile );
        const hiddenAnchor = document.createElement( "a" );
        hiddenAnchor.style.display = "none";
        hiddenAnchor.href = url;
        hiddenAnchor.download = filename;
        document.body.appendChild( a );
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
            // create: false
        } );
    }

}

class AjaxAction {
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
        this.getOption( 'category_product_lov_api', onSuccess )

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


// $( document ).ready( function () {
//     const payload = {
//         method: 'POST',
//         headers: {
//             'Content-type': 'application/json'
//         },
//         body: JSON.stringify( {
//             date_month: 2,
//             date_year: 2022
//         } )
//     }
//     fetch( 'report_transaction_purchased', payload )
//         .then( response => response.json() ).then( resp => {
//             const convertedExcelToBuffer = base64DecToArr( resp.data ).buffer;
//             const excelInBlob = new Blob( [ convertedExcelToBuffer ] )
//             downloadExcelSilently( excelInBlob, 'index.xlsx' )

//         } )


// } )

