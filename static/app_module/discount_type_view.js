class DatatableDiscountTypeImpl extends BaseDatatable {
    constructor() {
        super()
        this.tableColumns = [
            {
                data: null,
                defaultContent: ''
            },
            { data: 'discount_type_id' },
            { data: 'discount_type' },
            {
                data: 'active_status',
                render: ( data ) => {
                    if ( data == 'Y' ) return 'Active';
                    return 'Non-Active'
                }
            }
        ]
        this.columnName = [
            { "name": "no", "targets": 0 },
            { "name": "discount_type_id", "targets": 1 },
            { "name": "discount_type", "targets": 2 },
            { "name": "active_status", "targets": 3 }
        ]
        this.datatableId = '#discount_type_datatable_id'
        this.apiEndpoint = '/discount_type_api'
    }
    getTableSetup() {
        const tableSetup = {
            ajax: {
                url: this.apiEndpoint,
                method: 'GET'
            },
            processing: true,
            serverSide: true,
            columns: this.tableColumns,
            columnDefs: this.columnName,
            order: [ [ 1, 'asc' ] ],
            dom: this.toolbarDomConfig.top + this.toolbarDomConfig.table + this.toolbarDomConfig.bottom,
            fnInitComplete: () => { }
        }
        return tableSetup
    }
}


const runScript = () => {
    $( document ).ready( function () {
        new DatatableDiscountTypeImpl().initiateDatatable()
    } )
}

runScript()
