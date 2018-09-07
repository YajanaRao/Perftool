function tabulate(data, columns) {
            var table = d3.select('div.sys-table').append('table')
            var thead = table.append('thead')
            var tbody = table.append('tbody')

            // Append header row
            thead.append('tr').selectAll('th').data(columns).enter().append('th').text(function (column) { return column; });
            d3.selectAll('table').classed("w3-table-all w3-hoverable", true)
            // create a row for each object in the data
            var rows = tbody.selectAll('tr')
                .data(data)
                .enter()
                .append('tr');

            // create a cell in each row for each column
            var cells = rows.selectAll('td')
                .data(function (row) {
                    return columns.map(function (column) {
                        return { column: column, value: row[column] };
                    });
                })
                .enter()
                .append('td')
                .text(function (d) { return d.value; });

            return table;
        }

        d3.csv("systemdata.csv", function (error, data) {
            if (error) throw error;

            tabulate(data, ['System', 'Information'])


            // format the data
            data.forEach(function (d) {
                console.log(d)
            });
        });

        d3.csv("performancedata.csv", function (error, data) {
            if (error) throw error;


            // get data
            var time = []
            var cpu = []
            var memory = []
            var disk = []
            console.log(time)
            data.forEach(function (d) {
                time.push(d.time);
                memory.push(d.memory);
                disk.push(d.disk);
                cpu.push(d.cpu)
                console.log(d.time, d.disk, d.memory)
            });
            console.log(time, cpu, memory);
            var ctx = document.getElementById("myChart").getContext('2d');
            var myChart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: time,
                    datasets: [{
                        label: '# CPU',
                        data: cpu,
                        backgroundColor: [
                            'rgba(255, 99, 132, 0.2)'
                        ],
                        borderColor: [
                            'rgba(255,99,132,1)'
                        ],
                        borderWidth: 1
                    },
                    {
                        label: '# Memory',
                        data: memory,
                        backgroundColor: [
                            'rgba(54, 162, 235, 0.2)'
                        ],
                        borderColor: [
                            'rgba(54, 162, 235, 1)'
                        ],
                        borderWidth: 1
                    },
                    {
                        label: '# Disk',
                        data: disk,
                        backgroundColor: [
                            'rgba(255, 206, 86, 0.2)'
                        ],
                        borderColor: [
                            'rgba(255, 206, 86, 1)'
                        ],
                        borderWidth: 1
                    }
                    ]
                },
                options: {
                    responsive: false,
                    scales: {
                        yAxes: [{
                            ticks: {
                                max: 100,
                                min: 0
                            },
                            scaleLabel: {
                                display: true,
                                labelString: 'Percentage (%) '
                            },
                        }],
                        xAxes: [{

                            scaleLabel: {
                                display: true,
                                labelString: 'Time'
                            },
                        }]
                    }

                }
            });

        });

        d3.csv("processdata.csv", function (error, data) {
            if (error) throw error;


            // get data
            var time = []
            var cpu = []
            var memory = []
            console.log(time)
            data.forEach(function (d) {
                time.push(d.time);
                memory.push(d.memory);
                cpu.push(d.cpu)
                console.log(d.time, d.cpu, d.memory)
            });
            console.log(time, cpu, memory);
            var ctx = document.getElementById("processChart").getContext('2d');
            var myChart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: time,
                    datasets: [{
                        label: '# CPU',
                        data: cpu,
                        backgroundColor: [
                            'rgba(255, 99, 132, 0.2)'
                        ],
                        borderColor: [
                            'rgba(255,99,132,1)'
                        ],
                        borderWidth: 1
                    },
                    {
                        label: '# Memory',
                        data: memory,
                        backgroundColor: [
                            'rgba(54, 162, 235, 0.2)'
                        ],
                        borderColor: [
                            'rgba(54, 162, 235, 1)'
                        ],
                        borderWidth: 1
                    }
                    ]
                },
                options: {
                    responsive: false,
                    scales: {
                        yAxes: [{
                            ticks: {
                                max: 100,
                                min: 0
                            },
                            scaleLabel: {
                                display: true,
                                labelString: 'Percentage (%)'
                            },
                        }],
                        xAxes: [{
                            scaleLabel: {
                                display: true,
                                labelString: 'Time'
                            },
                        }]
                    }

                }
            });

            d3.csv("networkdata.csv", function (error, data) {
                if (error) throw error;


                // get data
                var time = []
                var sent = []
                var recv = []
                console.log(time)
                data.forEach(function (d) {
                    time.push(d.time);
                    sent.push(d.sent);
                    recv.push(d.recv)
                    console.log(d.time, d.cpu, d.memory)
                });
                console.log(time, sent, recv);
                var ctx = document.getElementById("networkChart").getContext('2d');
                var myChart = new Chart(ctx, {
                    type: 'line',
                    data: {
                        labels: time,
                        datasets: [{
                            label: '# SENT',
                            data: sent,
                            backgroundColor: [
                                'rgba(255, 99, 132, 0.2)'
                            ],
                            borderColor: [
                                'rgba(255,99,132,1)'
                            ],
                            borderWidth: 1
                        },
                        {
                            label: '# RECV',
                            data: recv,
                            backgroundColor: [
                                'rgba(54, 162, 235, 0.2)'
                            ],
                            borderColor: [
                                'rgba(54, 162, 235, 1)'
                            ],
                            borderWidth: 1
                        }
                        ]
                    },
                    options: {
                        responsive: false,
                        scales: {
                            yAxes: [{
                                // ticks: {
                                //     max: 1,
                                //     min: 0
                                // },
                                scaleLabel: {
                                    display: true,
                                    labelString: 'MB'
                                },
                            }],
                            xAxes: [{
                                scaleLabel: {
                                    display: true,
                                    labelString: 'Time'
                                },
                            }]
                        }

                    }
                });

            });

        });
