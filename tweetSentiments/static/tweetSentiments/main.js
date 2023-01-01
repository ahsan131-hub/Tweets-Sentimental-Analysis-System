console.log("scripting is connected....!")
let stats = {}
let keyword = ""
var modal = document.getElementById("myModal");


//Would make strUser be 2.
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');
//   method: 'POST',
//     credentials: 'same-origin',
//     headers:{
//         'Accept': 'application/json',
//         'X-Requested-With': 'XMLHttpRequest', //Necessary to work with request.is_ajax()
//         'X-CSRFToken': csrftoken,
// },
//     body: JSON.stringify({'post_data':'Data to post'})
const graphBtn = document.getElementById("showGraphBtn")
const closePopup = document.getElementById("closePopup")
let myChart = null;
graphBtn.onclick = () => {

    const ctx = document.getElementById('myChart').getContext('2d');
    Chart.defaults.color = "white";
    modal.style.display = "block"
    myChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ["positive", "negative", "neutral"],
            datasets: [{
                label: `Analysis of ${keyword}`,
                data: [stats.positive, stats.negative, stats.neutral],
                backgroundColor: [
                    'rgb(165,255,121)',
                    'rgb(255, 99, 132)',
                    'rgb(253,185,118)',
                ],
                borderColor: [
                    'rgb(255, 99, 132)',
                    'rgb(255, 159, 64)',
                    'rgb(75, 192, 192)',
                ],
                borderWidth: 1,
                hoverOffset: 4
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            },
            defaults: {
                color: "white"
            },
            responsive: true, scaleFontColor: "#FFFFFF",
            plugins: {
                legend: {
                    labels: {
                        // This more specific font property overrides the global property
                        font: {
                            size: 30,

                        }

                    }
                }
            }
        }
    });
    myChart.defaults.color = "white"
    modal.style.display = "block"
}

window.onclick = function (event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}

const onSubmit = (event) => {
    event.preventDefault();
    if (myChart) myChart.destroy()

    const from = document.getElementById("fromDate").value
    const to = document.getElementById("toDate").value
    const keywords = document.getElementById("searchbar").value
    const numOfTweets = document.getElementById("numberOfTweets").value
    const model = document.getElementById("modelSelection").value

    if (!keywords || !from || !to) {
        alert("Pleas type some keywords...")
        return
    }
    keyword = keywords
    console.log(from + "" + to)
    document.getElementById("loading-div").classList.remove("hidden")
    removeElementsByClass("tweet")
    console.log("{% url 'results' %}")
    fetch("evaluate/",
        {
            method: 'POST',
            credentials: 'same-origin',
            headers: {
                'Accept': 'application/json',
                'X-Requested-With': 'XMLHttpRequest', //Necessary to work with request.is_ajax()
                'X-CSRFToken': csrftoken,
                csrfmiddlewaretoken: csrftoken
            },
            body: JSON.stringify({
                'keywords': keywords,
                "fromDate": from.toString(),
                "toDate": to.toString(),
                "limit": numOfTweets || 100,
                "model": model
            })
        }).then(res => res.json()).then(data => {
        document.getElementById("loading-div").classList.add("hidden")
        let tweets_div = document.getElementsByClassName("tweets")[0]
        console.log(data)
        // console.log(data?.stats_array)
        data.data.forEach((tweet, number) => {
            let template = document.createElement("div")
            template.classList.add("tweet")
            template.innerHTML = `
                <div class="tweet-heading">
                    <div class="date ">
                       ${tweet.date}
                    </div>
                    
                    <div class="author "> ${number + 1}</div>
                </div>
                <div class="tweet-content">
                   ${tweet.tweet}
                </div>
            `
            tweets_div.appendChild(template)
        })
        stats = data.stats
    })
}

function removeElementsByClass(className) {
    const elements = document.getElementsByClassName(className);
    while (elements.length > 0) {
        elements[0].parentNode.removeChild(elements[0]);
    }
}

document.getElementById("tweet-submit").onsubmit = onSubmit

