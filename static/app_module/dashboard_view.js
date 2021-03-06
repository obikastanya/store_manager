$( document ).ready( function () {
    const dashboard = new DashboardViews()
    dashboard.loadDefaultCharts()
    dashboard.loadBadgeData()
    dashboard.addListenerWhenCardButtonClicked()
    dashboard.addListenerWhenFilterChanged()
    dashboard.setAsActiveMenu()
} )


class DashboardViews {
    setAsActiveMenu() {
        document.querySelector( '#dashboard_side_link' ).classList.add( 'active' )
    }
    loadDefaultCharts() {
        this.showPurchasedVsSoldChartSummary()
    }
    loadBadgeData() {
        let setCardValuesAfterAjax = ( response ) => {
            new DashboardViews().setCardValues( response.data[ 0 ] )
        }
        new AjaxActions().getShortSummaryOfAll().then( setCardValuesAfterAjax )
    }
    addListenerWhenCardButtonClicked() {
        let soldVsPurchasedCardBtn = document.querySelector( "#sold_vs_purchased_card_btn" )
        soldVsPurchasedCardBtn.addEventListener( 'click', new DashboardViews().showPurchasedVsSoldChartSummary )

        let soldCardBtn = document.querySelector( "#sold_card_btn" )
        soldCardBtn.addEventListener( 'click', new DashboardViews().showSoldChartSummary )

        let purchasedCardBtn = document.querySelector( "#purchased_card_btn" )
        purchasedCardBtn.addEventListener( 'click', new DashboardViews().showPurchasedChartSummary )

        let availabilityProductCardBtn = document.querySelector( "#availability_product_card_btn" )
        availabilityProductCardBtn.addEventListener( 'click', new DashboardViews().showAvailabilityChartSummary )
    }
    addListenerWhenFilterChanged() {
        let monthField = document.querySelector( "#monthFields" )
        monthField.addEventListener( 'change', new DashboardViews().refreshChartWhenFilterChanged )

        let yearField = document.querySelector( "#yearFields" )
        yearField.addEventListener( 'change', new DashboardViews().refreshChartWhenFilterChanged )

    }
    showPurchasedVsSoldChartSummary() {
        const dashboard = new DashboardViews()
        const paramFilter = dashboard.getChartFilter()
        dashboard.setCanvasLabel( 'Purchased vs Sold Product', 'Composition of Product Sold' )
        dashboard.setActiveChart( 'purchased_vs_sold' )
        dashboard.adjustLabelsClassHeight( 4 )
        dashboard.setAreaChartLabels( false )
        dashboard.refreshAllCanvas()

        const createLineCharts = ( response ) => {
            new LineChart().initiate( "myAreaChart", response )
        }
        const createPieCharts = ( response ) => {
            new DonutChart().initiate( "myPieChart", response )
            new DashboardViews().setPieChartLabels( response.data )
        }

        new AjaxActions().getSoldVsPurchasedSummary( paramFilter ).then( createLineCharts )
        new AjaxActions().getSoldVsPurchasedSummaryGroupByCategory( paramFilter ).then( createPieCharts )
    }
    showPurchasedChartSummary() {
        const dashboard = new DashboardViews()
        const paramFilter = dashboard.getChartFilter()
        dashboard.setActiveChart( 'purchased_summary' )
        dashboard.setCanvasLabel( 'Purchased Product Transaction', 'Composition of Purchased Transaction' )
        dashboard.adjustLabelsClassHeight( 4 )
        dashboard.setAreaChartLabels( false )
        dashboard.refreshAllCanvas()

        const createLineCharts = ( response ) => {
            new BarChartRed().initiate( "myAreaChart", response )
        }
        const createPieCharts = ( response ) => {
            new PieChart().initiate( "myPieChart", response )
            new DashboardViews().setPieChartLabels( response.data )
        }


        new AjaxActions().getProductPurchasedSummary( paramFilter ).then( createLineCharts )
        new AjaxActions().getProductPurchasedSummaryGroupByCategory( paramFilter ).then( createPieCharts )
    }
    showSoldChartSummary() {
        const dashboard = new DashboardViews()
        const paramFilter = dashboard.getChartFilter()
        dashboard.setActiveChart( 'sold_summary' )
        dashboard.setCanvasLabel( 'Sold Product Transaction', 'Composition of Sold Transaction' )
        dashboard.adjustLabelsClassHeight( 4 )
        dashboard.setAreaChartLabels( false )
        dashboard.refreshAllCanvas()

        const createBarCharts = ( response ) => {
            new BarChart().initiate( "myAreaChart", response )
        }
        const createPieCharts = ( response ) => {
            new PieChart().initiate( "myPieChart", response )
            new DashboardViews().setPieChartLabels( response.data )
        }


        new AjaxActions().getProductSoldSummary( paramFilter ).then( createBarCharts )
        new AjaxActions().getProductSoldSummaryGroupByCategory( paramFilter ).then( createPieCharts )
    }
    showAvailabilityChartSummary() {
        const dashboard = new DashboardViews()
        const paramFilter = dashboard.getChartFilter()
        dashboard.setActiveChart( 'availability_store_summary' )
        dashboard.setCanvasLabel( 'Availability Product Store', 'Availability Product Warehouse' )
        dashboard.adjustLabelsClassHeight( 2 )
        dashboard.refreshAllCanvas()

        const createBigPieCharts = ( response ) => {
            new PieChart().initiate( "myAreaChart", response )
            new DashboardViews().setAreaChartLabels( response.data )
        }
        const createPieCharts = ( response ) => {
            new PieChart().initiate( "myPieChart", response )
            new DashboardViews().setPieChartLabels( response.data )
        }
        new AjaxActions().getProductAvailabilityStoreSummary( paramFilter ).then( createBigPieCharts )
        new AjaxActions().getProductAvailabilityWarehouseSummary( paramFilter ).then( createPieCharts )
    }
    getChartFilter() {
        const getDataFromId = ( idElement ) => {
            return document.querySelector( idElement ).value
        }
        const dataFilter = {
            date_month: getDataFromId( '#monthFields' ),
            date_year: getDataFromId( '#yearFields' )
        }
        return dataFilter
    }
    setCardValues( record ) {
        document.querySelector( "#cash_out_card" ).innerHTML = `${ new DashboardViews().formatTotalCash( record.total_cash_out ) } Cash Out`
        document.querySelector( "#cash_in_card" ).innerHTML = `${ new DashboardViews().formatTotalCash( record.total_cash_in ) } Cash In`
        document.querySelector( "#transaction_sold_card" ).innerHTML = `${ record.total_transaction_product_sold } Transaction`
        document.querySelector( "#transaction_purchased_card" ).innerHTML = `${ record.total_transaction_product_purchased } Transaction`
        document.querySelector( "#availability_product_card" ).innerHTML = `${ record.total_product_in_store } Product`
    }
    setActiveChart( activeChart ) {
        document.querySelector( "#activeChart" ).value = activeChart
    }

    formatTotalCash( totalCash ) {
        let removedZeroPrecision = totalCash.split( "." )[ 0 ]
        if ( removedZeroPrecision.length > 4 ) {
            return removedZeroPrecision.slice( 0, -3 ) + 'K'
        }
        return removedZeroPrecision
    }
    setPieChartLabels( rawData ) {
        let labels = ''
        let count = 0
        let colorList = [ '#4e73df', '#36b9cc', '#1cc88a', '#F6C23E', '#FE777B', '#FF9F40', '#9C8BCD', '#9D5454', '#96CEB4', '#BAFFB4' ]
        for ( let records of rawData ) {
            labels += `
                <span class="mr-2">
                <i class="fas fa-circle" style='color:${ colorList[ count ] };'></i> ${ records.data_key }
                </span>`
            count++;
        }
        document.querySelector( '#pie_chart_labels' ).innerHTML = labels
    }
    setAreaChartLabels( rawData ) {
        if ( !rawData ) {
            document.querySelector( '#area_chart_labels' ).innerHTML = ''
            return
        }
        let labels = ''
        let count = 0
        let colorList = [ '#4e73df', '#36b9cc', '#1cc88a', '#F6C23E', '#FE777B', '#FF9F40', '#9C8BCD', '#9D5454', '#96CEB4', '#BAFFB4' ]
        for ( let records of rawData ) {
            labels += `
                <span class="mr-2">
                <i class="fas fa-circle" style='color:${ colorList[ count ] };'></i> ${ records.data_key }
                </span>`
            count++;
        }
        document.querySelector( '#area_chart_labels' ).innerHTML = labels
    }
    refreshAllCanvas() {
        this.refreshCanvas( 'myAreaChart-container', 'myAreaChart' )
        this.refreshCanvas( 'myPieChart-container', 'myPieChart' )
    }
    refreshCanvas( containerClass, canvasId ) {
        var canvasContainer = document.querySelector( `.${ containerClass }` );
        canvasContainer.innerHTML = `<canvas id='${ canvasId }'></canvas>`
    }
    setCanvasLabel( areaTittle, pieTittle ) {
        document.querySelector( '#area_canvas_title' ).innerHTML = areaTittle
        document.querySelector( '#pie_canvas_title' ).innerHTML = pieTittle
    }
    adjustLabelsClassHeight( marginNumber ) {

        let containerOfAreaLabels = document.querySelector( "#area_chart_labels" )
        containerOfAreaLabels.classList.remove( 'mt-2' )
        containerOfAreaLabels.classList.remove( 'mt-4' )

        // adding class
        if ( marginNumber == 2 ) {
            containerOfAreaLabels.classList.add( 'mt-2' )
            return
        }
        containerOfAreaLabels.classList.add( 'mt-4' )
        return
    }
    refreshChartWhenFilterChanged() {
        const activeChart = document.querySelector( '#activeChart' ).value
        const dashboard = new DashboardViews()
        if ( activeChart == 'purchased_vs_sold' ) return dashboard.showPurchasedVsSoldChartSummary();
        if ( activeChart == 'sold_summary' ) return dashboard.showSoldChartSummary();
        if ( activeChart == 'purchased_summary' ) return dashboard.showPurchasedChartSummary();
        if ( activeChart == 'availability_store_summary' ) return dashboard.showAvailabilityChartSummary();
    }

}

class AjaxActions {
    getSoldVsPurchasedSummary( protoPayload ) {
        const payload = this.createPayload( { ...{ summarize_type: 'purchased_vs_sold' }, ...protoPayload } )
        return this.sendAjax( '/dashboard_api', payload )
    }
    getShortSummaryOfAll( protoPayload ) {
        const payload = this.createPayload( { ...{ summarize_type: 'summarize_total' }, ...protoPayload } )
        return this.sendAjax( '/dashboard_api', payload )
    }
    getSoldVsPurchasedSummaryGroupByCategory( protoPayload ) {
        const payload = this.createPayload( { ...{ summarize_type: 'purchased_vs_sold', group_by_category: true }, ...protoPayload } )
        return this.sendAjax( '/dashboard_api', payload )
    }
    getProductSoldSummary( protoPayload ) {
        const payload = this.createPayload( { ...{ summarize_type: 'sold_summary' }, ...protoPayload } )
        return this.sendAjax( '/dashboard_api', payload )
    }
    getProductSoldSummaryGroupByCategory( protoPayload ) {
        const payload = this.createPayload( { ...{ summarize_type: 'sold_summary', group_by_category: true }, ...protoPayload } )
        return this.sendAjax( '/dashboard_api', payload )
    }
    getProductPurchasedSummary( protoPayload ) {
        const payload = this.createPayload( { ...{ summarize_type: 'purchased_summary' }, ...protoPayload } )
        return this.sendAjax( '/dashboard_api', payload )
    }
    getProductPurchasedSummaryGroupByCategory( protoPayload ) {
        const payload = this.createPayload( { ...{ summarize_type: 'purchased_summary', group_by_category: true }, ...protoPayload } )
        return this.sendAjax( '/dashboard_api', payload )
    }
    getProductAvailabilityStoreSummary( protoPayload ) {
        const payload = this.createPayload( { ...{ summarize_type: 'availability_store_summary' }, ...protoPayload } )
        return this.sendAjax( '/dashboard_api', payload )
    }
    getProductAvailabilityWarehouseSummary( protoPayload ) {
        const payload = this.createPayload( { ...{ summarize_type: 'availability_warehouse_summary' }, ...protoPayload } )
        return this.sendAjax( '/dashboard_api', payload )
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
    sendAjax( url, payload ) {
        return fetch( url, payload )
            .then( response => response.json() )
    }
}
class LineChart {

    initiate( canvasId, response ) {
        let theBiggerCanvas = document.getElementById( canvasId );
        let config = this.getDefaultConfig()
        config.data = this.generateDataForChart( response.data )
        new Chart( theBiggerCanvas, config )

    }
    getDefaultConfig() {
        let config = {
            type: 'line',
            options: {
                maintainAspectRatio: false,
                layout: {
                    padding: {
                        left: 10,
                        right: 25,
                        top: 25,
                        bottom: 0
                    }
                },
                scales: this.getScales(),
                legend: {
                    display: false
                }
            }
        }
        return config
    }
    getScales() {
        const scales = {
            xAxes: this.getxAxes(),
            yAxes: [ {
                ticks: {
                    maxTicksLimit: 5,
                    padding: 10
                },
                gridLines: this.getGridLines()
            } ],
        }
        return scales
    }

    getGridLines() {
        const gridLines = {
            color: "rgb(234, 236, 244)",
            zeroLineColor: "rgb(234, 236, 244)",
            drawBorder: false,
            borderDash: [ 2 ],
            zeroLineBorderDash: [ 2 ]
        }
        return gridLines
    }

    getxAxes() {
        const xAxes = [ {
            time: {
                unit: 'date'
            },
            gridLines: {
                display: false,
                drawBorder: false
            },
            ticks: {
                maxTicksLimit: 7
            }
        } ]
        return xAxes
    }
    generateDataForChart( rawData ) {
        let purchasedConfig = {
            data: [],
            fill: false,
            tension: 0.1,
            borderColor: 'rgb(75, 102, 92)',
            label: 'Cash Out'
        }

        let soldConfig = {
            data: [],
            fill: false,
            tension: 0.1,
            borderColor: 'rgb(75, 192, 192)',
            label: 'Cash In'
        }

        let labels = []
        for ( let records of rawData ) {
            labels.push( records.date_sold )
            purchasedConfig.data.push( records.product_purchased )
            soldConfig.data.push( records.product_sold )
        }

        // returning dataset
        return {
            labels: labels,
            datasets: [
                soldConfig,
                purchasedConfig
            ]
        }
    }
}

class PieChart {
    initiate( canvasId, response ) {
        var littleCanvas = document.getElementById( canvasId );
        let config = this.getDefaultConfig()
        config.data = this.generateDataForChart( response.data )
        new Chart( littleCanvas, config )
    }

    getDefaultConfig() {
        let config = {
            type: 'pie',
            data: [],
            options: this.getOptions()
        }

        return config
    }
    generateDataForChart( rawData ) {
        let dataConfig = {
            data: [],
            backgroundColor: [ '#4e73df', '#36b9cc', '#1cc88a', '#F6C23E', '#FE777B', '#FF9F40', '#9C8BCD', '#9D5454', '#96CEB4', '#BAFFB4' ],
            hoverBackgroundColor: [ '#2e59d9' ],
            hoverBorderColor: "rgba(234, 236, 244, 1)"
        }
        let labels = []
        for ( let records of rawData ) {
            labels.push( records.data_key )
            dataConfig.data.push( records.data_value )
        }

        // returning dataset
        return {
            labels: labels,
            datasets: [ dataConfig ]
        }
    }

    getOptions() {
        const options = {
            maintainAspectRatio: false,
            tooltips: {
                backgroundColor: "rgb(255,255,255)",
                bodyFontColor: "#858796",
                borderColor: '#dddfeb',
                borderWidth: 1,
                xPadding: 15,
                yPadding: 15,
                displayColors: false,
                caretPadding: 10,
            },
            legend: {
                display: false
            },
            cutoutPercentage: this.getCutOutPercentage(),
        }

        return options
    }
    getCutOutPercentage() {
        return 0
    }
}


class DonutChart extends PieChart {
    initiate( canvasId, response ) {
        var littleCanvas = document.getElementById( canvasId );
        let config = this.getDefaultConfig()
        config.data = this.generateDataForChart( response.data )
        new Chart( littleCanvas, config )
    }
    getDefaultConfig() {
        let config = {
            type: 'doughnut',
            data: [],
            options: this.getOptions()
        }
        return config
    }
    getCutOutPercentage() {
        return 75
    }


    generateDataForChart( rawData ) {
        let dataConfig = {
            data: [],
            backgroundColor: [ '#9C8BCD', '#4e73df', '#36b9cc', '#F6C23E', '#FE777B', '#FF9F40', '#96CEB4', '#BAFFB4', '#9D5454', '#1cc88a', ],
            hoverBackgroundColor: [ '#2e59d9' ],
            hoverBorderColor: "rgba(234, 236, 244, 1)"
        }
        let labels = []
        for ( let records of rawData ) {
            labels.push( records.data_key )
            dataConfig.data.push( records.data_value )
        }

        // returning dataset
        return {
            labels: labels,
            datasets: [ dataConfig ]
        }
    }
}
class BarChart {
    initiate( idCanvas, response ) {
        let canvas = document.getElementById( idCanvas );
        let config = this.getDefaultConfig()
        config.data = this.generateDataForChart( response.data )
        new Chart( canvas, config )
    }
    getDefaultConfig() {
        const config = {
            type: 'bar',
            options: {
                maintainAspectRatio: false,
                layout: {
                    padding: {
                        left: 10,
                        right: 25,
                        top: 25,
                        bottom: 0
                    }
                },
                scales: this.getScales(),
                legend: {
                    display: false
                },
                tooltip: this.getTooltip()
            }
        }
        return config
    }
    getTooltip() {
        const tooltip = {
            titleMarginBottom: 10,
            titleFontColor: '#6e707e',
            titleFontSize: 14,
            backgroundColor: "rgb(255,255,255)",
            bodyFontColor: "#858796",
            borderColor: '#dddfeb',
            borderWidth: 1,
            xPadding: 15,
            yPadding: 15,
            displayColors: false,
            caretPadding: 10,
            callbacks: {
                label: function ( tooltipItem, chart ) {
                    var datasetLabel = chart.datasets[ tooltipItem.datasetIndex ].label || '';
                    return datasetLabel + tooltipItem.yLabel;
                }
            }
        }

        return tooltip
    }
    getScales() {
        const yAxes = [
            {
                gridLines: {
                    color: "rgb(234, 236, 244)",
                    zeroLineColor: "rgb(234, 236, 244)",
                    drawBorder: false,
                    borderDash: [ 2 ],
                    zeroLineBorderDash: [ 2 ]
                }
            } ]

        const scales = {
            xAxes: [ {
                time: {
                    unit: 'month'
                },
                gridLines: {
                    display: false,
                    drawBorder: false
                },
                ticks: {
                    maxTicksLimit: 6
                },
                maxBarThickness: 25,
            } ],
            yAxes: yAxes
        }

        return scales
    }
    generateDataForChart( rawData ) {
        let labels = []
        let data = []
        for ( let record of rawData ) {
            labels.push( record.data_key )
            data.push( record.data_value )
        }

        const dataConfig = {
            labels: labels,
            datasets: [ {
                label: "Transaction",
                backgroundColor: "#4e73df",
                hoverBackgroundColor: "#2e59d9",
                borderColor: "#4e73df",
                data: data,
            } ]
        }
        return dataConfig
    }
}

class BarChartRed extends BarChart {
    generateDataForChart( rawData ) {
        let labels = []
        let data = []
        for ( let record of rawData ) {
            labels.push( record.data_key )
            data.push( record.data_value )
        }

        const dataConfig = {
            labels: labels,
            datasets: [ {
                label: "Transaction",
                backgroundColor: "#FF6384",
                hoverBackgroundColor: "#2e59d9",
                borderColor: "#FF6384",
                data: data,
            } ]
        }
        return dataConfig
    }
}