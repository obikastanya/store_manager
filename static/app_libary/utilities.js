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