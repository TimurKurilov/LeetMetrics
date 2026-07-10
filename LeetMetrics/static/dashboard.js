fetch(`/api/dashboard-data/${username}/`)
    .then(response => response.json())
    .then(data => {


        const dates = data.dates;
        const rating = data.rating;

        const easy = data.easy;
        const medium = data.medium;
        const hard = data.hard;



        /*
        ==========================
        Rating Smooth Line
        ==========================
        */


        const ratingChart = echarts.init(
            document.getElementById("rating-chart")
        );


        ratingChart.setOption({

            title:{
                text:"Contest Rating History"
            },

            tooltip:{
                trigger:"axis"
            },


            xAxis:{
                type:"category",
                data:dates
            },


            yAxis:{
                type:"value"
            },


            series:[
                {
                    name:"Rating",
                    type:"line",
                    smooth:true,
                    data:rating,
                    areaStyle:{}
                }
            ]

        });




        /*
        ==========================
        Pie Easy Medium Hard
        ==========================
        */


        const difficultyChart = echarts.init(
            document.getElementById("difficulty-chart")
        );


        difficultyChart.setOption({

            title:{
                text:"Problems Distribution",
                left:"center"
            },


            tooltip:{
                trigger:"item"
            },


            series:[

                {
                    type:"pie",

                    radius:"60%",


                    data:[

                        {
                            value:easy[easy.length-1],
                            name:"Easy"
                        },

                        {
                            value:medium[medium.length-1],
                            name:"Medium"
                        },


                        {
                            value:hard[hard.length-1],
                            name:"Hard"
                        }

                    ]

                }

            ]

        });




        /*
        ==========================
        Stacked Area
        ==========================
        */


        const solvedChart = echarts.init(
            document.getElementById("solved-chart")
        );


        solvedChart.setOption({

            title:{
                text:"Solved Growth"
            },


            tooltip:{
                trigger:"axis"
            },


            legend:{
                data:[
                    "Easy",
                    "Medium",
                    "Hard"
                ]
            },


            xAxis:{
                type:"category",
                data:dates
            },


            yAxis:{
                type:"value"
            },


            series:[

                {
                    name:"Easy",
                    type:"line",
                    stack:"total",
                    smooth:true,
                    data:easy,
                    areaStyle:{}
                },


                {
                    name:"Medium",
                    type:"line",
                    stack:"total",
                    smooth:true,
                    data:medium,
                    areaStyle:{}
                },


                {
                    name:"Hard",
                    type:"line",
                    stack:"total",
                    smooth:true,
                    data:hard,
                    areaStyle:{}
                }

            ]

        });





        /*
        ==========================
        Calendar Heatmap
        ==========================
        */


        const heatmapChart = echarts.init(
            document.getElementById("heatmap-chart")
        );


        let heatmapData = [];


        for(let i = 0; i < dates.length; i++){


            let solved = 0;


            if(i > 0){

                solved = data.total[i] - data.total[i-1];

            }


            heatmapData.push([
                dates[i],
                solved
            ]);

        }



        heatmapChart.setOption({

            title:{
                text:"Daily Activity"
            },


            tooltip:{},


            visualMap:{
                min:0,
                max:10,
                calculable:true,
                orient:"horizontal"
            },


            calendar:{

                range:"2026",

            },


            series:[

                {

                    type:"heatmap",

                    coordinateSystem:"calendar",

                    data:heatmapData

                }

            ]

        });



        window.addEventListener(
            "resize",
            ()=>{
                ratingChart.resize();
                difficultyChart.resize();
                solvedChart.resize();
                heatmapChart.resize();
            }
        );


    });