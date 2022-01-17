$( document ).ready( function () {
    new DashboardViews().loadDefaultCharts()
    new DashboardViews().addListenerWhenCardButtonClicked()
} )


class DashboardViews {
    loadDefaultCharts() {
        const createCharts = ( response ) => {
            new LineChart().initiate( "myAreaChart", response )
            new DonutChart().initiate( "myPieChart", response )
        }
        new AjaxActions().getSoldVsPurchasedSummary().then( createCharts )
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
    showPurchasedVsSoldChartSummary() {
        new DashboardViews().refreshAllCanvas()
        new LineChart().initiate( "myAreaChart", {} )
        new DonutChart().initiate( "myPieChart", {} )
    }
    showPurchasedChartSummary() {
        new DashboardViews().refreshAllCanvas()

        new BarChart().initiateRed( "myAreaChart", {} )
        new PieChart().initiate( "myPieChart", {} )
    }
    showSoldChartSummary() {
        new DashboardViews().refreshAllCanvas()

        new BarChart().initiate( "myAreaChart", {} )
        new PieChart().initiate( "myPieChart", {} )
    }
    showAvailabilityChartSummary() {
        new DashboardViews().refreshAllCanvas()

        new PieChart().initiate( "myAreaChart", {} )
        new PieChart().initiate( "myPieChart", {} )
    }
    refreshAllCanvas() {
        this.refreshCanvas( 'myAreaChart-container', 'myAreaChart' )
        this.refreshCanvas( 'myPieChart-container', 'myPieChart' )
    }
    refreshCanvas( containerClass, canvasId ) {
        var canvasContainer = document.querySelector( `.${ containerClass }` );
        canvasContainer.innerHTML = `<canvas id='${ canvasId }'></canvas>`
    }

}

class AjaxActions {
    getSoldVsPurchasedSummary() {
        return Promise.resolve( 1 )
    }
    getProductSoldSummary() { }
    getProductPurchasedSummary() { }
    getProductAvailabilitySummary() { }
}
class LineChart {

    initiate( canvasId, response ) {
        let theBiggerCanvas = document.getElementById( canvasId );
        let config = this.getDefaultConfig()
        let dummyData = this.getDummyData()
        config.data = dummyData

        // creating chart
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
    getDummyData() {
        const dummyData = {
            labels: [ "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec", "Dec2" ],
            datasets: [
                {
                    label: 'Product Sold',
                    data: [ 0, 10000, 5000, 15000, 10000, 20000, 15000, 25000, 20000, 30000, 25000, 40000, 49000 ],
                    fill: false,
                    borderColor: 'rgb(75, 192, 192)',
                    tension: 0.1
                },
                {
                    label: 'Purchased',
                    data: [ 0, 1000, 3000, 1500, 14000, 2000, 1500, 2500, 23000, 30200, 25030, 46000,49000 ],
                    fill: false,
                    borderColor: 'rgb(75, 102, 92)',
                    tension: 0.1
                }
            ],
        }
        return dummyData
    }
}

class PieChart {
    initiate( canvasId, response ) {
        var littleCanvas = document.getElementById( canvasId );
        let config = this.getDefaultConfig()
        config.data = this.getDummyData()

        // create chart
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

    getDummyData() {
        const dummyData = {
            labels: [ "Direct", "Referral", "Social" ],
            datasets: [ {
                data: [ 55, 30, 15 ],
                backgroundColor: [ '#4e73df', '#1cc88a', '#36b9cc' ],
                hoverBackgroundColor: [ '#2e59d9', '#17a673', '#2c9faf' ],
                hoverBorderColor: "rgba(234, 236, 244, 1)",
            } ],
        }

        return dummyData
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
    getDefaultConfig() {
        let config = {
            type: 'doughnut',
            data: [],
            options: this.getOptions()
        }
        return config
    }
    getCutOutPercentage() {
        return 80
    }
}
class BarChart {
    initiate( idCanvas ) {
        var ctx = document.getElementById( idCanvas );

        new Chart( ctx, this.getDefaultConfig() );
    }
    initiateRed( idCanvas ) {
        var ctx = document.getElementById( idCanvas );
        let config = this.getDefaultConfig()
        config.data = this.getDummyDataRed()
        new Chart( ctx, config );
    }
    getDefaultConfig() {
        const config = {
            type: 'bar',
            data: this.getDummyData(),
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
                scales: {
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
                    yAxes: [ {
                        ticks: {
                            min: 0,
                            max: 15000,
                            maxTicksLimit: 5,
                            padding: 10,
                            // Include a dollar sign in the ticks
                            callback: function ( value, index, values ) {
                                return '$' + value;
                            }
                        },
                        gridLines: {
                            color: "rgb(234, 236, 244)",
                            zeroLineColor: "rgb(234, 236, 244)",
                            drawBorder: false,
                            borderDash: [ 2 ],
                            zeroLineBorderDash: [ 2 ]
                        }
                    } ],
                },
                legend: {
                    display: false
                },
                tooltips: {
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
                            return datasetLabel + ': $' + tooltipItem.yLabel;
                        }
                    }
                },
            }
        }
        return config
    }
    getDummyData() {
        const dummyData = {
            labels: [ "January", "February", "March", "April", "May", "June", "July" ],
            datasets: [ {
                label: "Revenue",
                backgroundColor: this.getBlue(),
                hoverBackgroundColor: "#2e59d9",
                borderColor: this.getBlue(),
                data: [ 4215, 5312, 6251, 7841, 9821, 14984, 4522 ],
            } ],
        }
        return dummyData
    }
    getDummyDataRed() {
        const dummyData = {
            labels: [ "January", "February", "March", "April", "May", "June" ],
            datasets: [ {
                label: "Revenue",
                backgroundColor: this.getRed(),
                hoverBackgroundColor: "#2e59d9",
                borderColor: this.getRed(),
                data: [ 4215, 5312, 6251, 7841, 9821, 14984 ],
            } ],
        }
        return dummyData
    }

    getRed() {
        return "#FF6384"
    }
    getBlue() {
        return "#4e73df"
    }

}