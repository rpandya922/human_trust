/*
 * Requires:
 *     psiturk.js
 *     utils.js
 */

// Initalize psiturk object
var psiTurk = new PsiTurk(uniqueId, adServerLoc, mode);

var mycondition = condition;  // these two variables are passed by the psiturk server process
var mycounterbalance = counterbalance;  // they tell you which condition you have been assigned to
var stats; // determines what statistics to show the person; 0: none, 1: avg + std dev, 2: previous 4
// they are not used in the stroop code but may be useful to you
// console.log(mycondition);
// All pages to be loaded

////////////////////////////////////////////////////////////////////////////////////////////////////////
// for real study, should be =30
const NUM_ITERATIONS = 30;
// const EXPERIMENT_TYPE = "stats";
const EXPERIMENT_TYPE = "observe";
if (EXPERIMENT_TYPE == "stats") {
    // set stats variable to condition passed in
    stats = condition;

    // put code into only-collaborate mode
    mycondition = 1;
} else if (EXPERIMENT_TYPE == "observe") {
    // put code into showing-previous-4 mode   
    stats = 2;

    // set condition to passed in condition
    mycondition = condition;
}
// delete for real study
// mycondition = 0;
////////////////////////////////////////////////////////////////////////////////////////////////////////

var pages = [
    "instructions/instruct-1.html",
    "instructions/instruct-2.html",
    "instructions/instruct-3.html",
    "multiarm_bandit.html",
    "multiarm_bandit_easy.html",
    "multiarm_bandit_hard.html",
    "observe_learning.html",
    "observe_learning_easy.html",
    "observe_learning_hard.html",
    "between_conditions.html", 
    "postquestionnaire.html",
    "testing_questionnaire.html",
    "robot_question.html"
];

psiTurk.preloadPages(pages);

var instructionPages = [ // add as a list as many pages as you like
    "instructions/instruct-1.html",
    "instructions/instruct-2.html"
];

if (EXPERIMENT_TYPE == "stats" && stats == 1) {
    instructionPages = [
        "instructions/instruct-1.html",
        "instructions/instruct-3.html",  
        "instructions/instruct-2.html"  
    ];
}

/********************
* Constants
*********************/
var DEFAULT_COLOR = 'btn-secondary';
var HIGHLIGHT_COLOR = 'btn-primary';
var GREEDY_COLOR = 'btn-success';
var GREEDY2_COLOR = 'btn-danger';
var OPTIMAL_COLOR = 'btn-primary';
var RANDOM_COLOR = 'btn-warning';

const BAD_COLOR = "#000000";
const OKAY_COLOR = "#6C6C6C";
const GOOD_COLOR = "#D9D9D9";
// const BAD_COLOR = "#E5001E";
// const OKAY_COLOR = "#D2B800";
// const GOOD_COLOR = "#16BF00";


function shuffle(a) {
    for (let i = a.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [a[i], a[j]] = [a[j], a[i]];
    }
    return a;
}
function match_shuffle(a, order) {
    var ret = [];
    for (i = 0; i < order.length; i++) {
        ret.push(a[order[i]]);
    }
    return ret;
}
////////////////////////////////////////////////////////////////////////////////////////////////////////
// Make sure color and order are shuffled the same way: uncomment for real study
var robot_shuffle_order = shuffle(_.range(4));
var robot_order = ["optimal2"];
var robot_colors = ["Red"];
////////////////////////////////////////////////////////////////////////////////////////////////////////

////////////////////////////////////////////////////////////////////////////////////////////////////////
// For debugging/testing, order stays the same: comment out for real study
// var robot_order = ["greedy", "optimal", "optimal2", "random"];
// var robot_colors = ["Green", "Blue", "Red", "Yellow"];
////////////////////////////////////////////////////////////////////////////////////////////////////////

// console.log(robot_order);
// console.log(robot_colors);
var difficulty_order = ["hard"];
var observation_difficulty_order = ["hard"];
var collaboration_order = ["suggest", "turns"];
var colors_easy = [GOOD_COLOR, BAD_COLOR];
var colors_worth_easy = ["Good", "Bad"];
var colors_medium = [GOOD_COLOR, OKAY_COLOR, OKAY_COLOR, BAD_COLOR];
var colors_worth_medium = ["Good", "Okay", "Okay", "Bad"];
// var colors_hard = ["#16BF00", "#43C300", "#71C700", "#A1CB00", "#CFCC00",
//                 "#D4A100", "#D87400", "#DC4500", "#E01400", "#E5001E"];
// var colors_hard = [GOOD_COLOR, GOOD_COLOR, GOOD_COLOR, OKAY_COLOR, OKAY_COLOR,
//                 OKAY_COLOR, OKAY_COLOR, BAD_COLOR, BAD_COLOR, BAD_COLOR];
// var colors_worth_hard = ["Good", "Good", "Good", "Okay", "Okay", "Okay", "Okay", "Bad", "Bad", "Bad"];
// var colors_hard = [GOOD_COLOR, GOOD_COLOR, OKAY_COLOR, OKAY_COLOR, BAD_COLOR, BAD_COLOR];
// var colors_worth_hard = ["Good", "Good", "Okay", "Okay", "Bad", "Bad"];
var colors_hard = [GOOD_COLOR, OKAY_COLOR, OKAY_COLOR, BAD_COLOR, BAD_COLOR, BAD_COLOR];
var colors_worth_hard = ["Good", "Okay", "Okay", "Bad", "Bad", "Bad"];
var human_selection;

var casino_names = ["A", ["B", "C"], ["D", "E"], ["F", "G"], ["H", "I"]];
if (mycondition == 1) {
    var casino_names = ["A", ["B", "B"], ["C", "C"], ["C", "C"], ["D", "D"]];
}

var stddev = function(arr) {
    if (arr.length == 0) {
        return 0;
    }
    var total = 0;
    for(var key in arr) 
       total += arr[key];
    var meanVal = total / arr.length;
  
    //--CALCULATE STANDARD DEVIATION--
    var SDprep = 0;
    for(var key in arr) 
       SDprep += Math.pow((parseFloat(arr[key]) - meanVal),2);
    var SDresult = Math.sqrt(SDprep/arr.length);
    //--CALCULATE STANDARD DEVIATION--
    return SDresult;
}
var argmax = function(arr) {
    var best = -1;
    var best_idx;
    for (var i = 0; i < arr.length; i++) {
        x = arr[i];
        if (x >= best) {
            best_idx = i;
            best = x;
        }
    }
    return best_idx;
};
var all_argmax = function(arr) {
    var max = Math.max(...arr);
    var best_idxs = [];
    for (var i = 0; i < arr.length; i++) {
        if (arr[i] == max) {
            best_idxs.push(i);
        }
    }
    return best_idxs;
};
var all_except_argmax = function(arr) {
    var max = Math.max(...arr);
    var idxs = [];
    for (var i = 0; i < arr.length; i++) {
        if (arr[i] != max) {
            idxs.push(i);
        }
    }
    if (idxs.length == 0) {
        // means all values were equal to max, so forced to highlight all
        return _.range(arr.length);
    }
    return idxs;
};
var highlight_arms = function(arms) {
    for(var i = 0; i < arms.length; i++) {
        document.getElementById("arm-" + String(arms[i])).classList.remove(DEFAULT_COLOR);
        document.getElementById("arm-" + String(arms[i])).classList.add(HIGHLIGHT_COLOR);
    }
};
var unhighlight_arms = function(arms) {
    for(var i = 0; i < arms.length; i++) {
        try {
            document.getElementById("arm-" + String(arms[i])).classList.remove(HIGHLIGHT_COLOR);
        } finally {
            document.getElementById("arm-" + String(arms[i])).classList.add(DEFAULT_COLOR);
        }
    }
};
var initialize_arms_matrix = function(difficulty, robot_color, condition) {
    // all payoffs and probabilities were randomly generated (with fixed expected rewards across robots)
    // hard coded because javascript can't seed random numbers
    if (robot_color == "Green") {
        if (condition == "observe") {
            if (difficulty == "hard") {
                // [ 1.   1.   1.5  1.5  2.9  1. ]
                return [[ 0.33333333,  0.5       ,  0.        ,  0.16666667,  0.        ],
                       [ 0.6875    ,  0.        ,  0.125     ,  0.        ,  0.1875    ],
                       [ 0.44444444,  0.        ,  0.16666667,  0.38888889,  0.        ],
                       [ 0.25      ,  0.        ,  0.75      ,  0.        ,  0.        ],
                       [ 0.18125   ,  0.        ,  0.        ,  0.375     ,  0.44375   ],
                       [ 0.61111111,  0.08333333,  0.        ,  0.30555556,  0.        ]];
            }
        } else if (condition == "collaborate") {
            if (difficulty == "hard") {
                // [ 1.5  1.   1.5  1.   2.9  1. ]
                return [[ 0.625     ,  0.        ,  0.        ,  0.        ,  0.375     ],
                       [ 0.6875    ,  0.        ,  0.        ,  0.25      ,  0.0625    ],
                       [ 0.58333333,  0.        ,  0.        ,  0.16666667,  0.25      ],
                       [ 0.59375   ,  0.        ,  0.3125    ,  0.        ,  0.09375   ],
                       [ 0.1375    ,  0.        ,  0.        ,  0.55      ,  0.3125    ],
                       [ 0.05555556,  0.91666667,  0.        ,  0.02777778,  0.        ]];
            }
        }
    } else if (robot_color == "Red") {
        if (condition == "observe") {
            if (difficulty == "hard") {
                // [ 1.5  1.5  1.   1.   1.   2.9]
                return [[ 0.        ,  0.5       ,  0.5       ,  0.        ,  0.        ],
                       [ 0.515625  ,  0.        ,  0.        ,  0.4375    ,  0.046875  ],
                       [ 0.66666667,  0.        ,  0.        ,  0.33333333,  0.        ],
                       [ 0.421875  ,  0.4375    ,  0.        ,  0.        ,  0.140625  ],
                       [ 0.5       ,  0.25      ,  0.        ,  0.25      ,  0.        ],
                       [ 0.1375    ,  0.        ,  0.        ,  0.55      ,  0.3125    ]];
            }
        } else if (condition == "collaborate") {
            if (difficulty == "hard") {
                // [ 1.5  1.   2.9  1.   1.5  1. ]
                return [[ 0.5       ,  0.        ,  0.25      ,  0.        ,  0.25      ],
                       [ 0.05555556,  0.91666667,  0.        ,  0.02777778,  0.        ],
                       [ 0.15      ,  0.        ,  0.        ,  0.5       ,  0.35      ],
                       [ 0.72916667,  0.        ,  0.        ,  0.08333333,  0.1875    ],
                       [ 0.        ,  0.5       ,  0.5       ,  0.        ,  0.        ],
                       [ 0.58333333,  0.        ,  0.25      ,  0.16666667,  0.        ]];
            }
        }
    } else if (robot_color == "Blue") {
        if (condition == "observe") {
            if (difficulty == "hard") {
                // [ 1.5  1.5  1.   1.   2.9  1. ]
                return [[ 0.125     ,  0.25      ,  0.625     ,  0.        ,  0.        ],
                       [ 0.27777778,  0.        ,  0.66666667,  0.05555556,  0.        ],
                       [ 0.55555556,  0.16666667,  0.        ,  0.27777778,  0.        ],
                       [ 0.11111111,  0.83333333,  0.        ,  0.05555556,  0.        ],
                       [ 0.17916667,  0.        ,  0.        ,  0.38333333,  0.4375    ],
                       [ 0.625     ,  0.        ,  0.125     ,  0.25      ,  0.        ]];
            }
        } else if (condition == "collaborate") {
            if (difficulty == "hard") {
                // [ 2.9  1.   1.   1.   1.5  1.5]
                return [[ 0.24375   ,  0.        ,  0.        ,  0.125     ,  0.63125   ],
                       [ 0.125     ,  0.75      ,  0.125     ,  0.        ,  0.        ],
                       [ 0.52777778,  0.        ,  0.41666667,  0.05555556,  0.        ],
                       [ 0.25      ,  0.5       ,  0.25      ,  0.        ,  0.        ],
                       [ 0.47222222,  0.        ,  0.08333333,  0.44444444,  0.        ],
                       [ 0.578125  ,  0.0625    ,  0.        ,  0.        ,  0.359375  ]];
            }
        }
    } else if (robot_color == "Yellow") {
        if (condition == "observe") {
            if (difficulty == "hard") {
                // [ 1.   1.   1.   1.5  2.9  1.5]
                return [[ 0.25      ,  0.5       ,  0.25      ,  0.        ,  0.        ],
                       [ 0.33333333,  0.5       ,  0.        ,  0.16666667,  0.        ],
                       [ 0.375     ,  0.5       ,  0.        ,  0.        ,  0.125     ],
                       [ 0.125     ,  0.25      ,  0.625     ,  0.        ,  0.        ],
                       [ 0.00555556,  0.        ,  0.08333333,  0.91111111,  0.        ],
                       [ 0.41666667,  0.        ,  0.25      ,  0.33333333,  0.        ]];
            }
        } else if (condition == "collaborate") {
            if (difficulty == "hard") {
                // [ 1.   1.   1.5  2.9  1.   1.5]
                return [[ 0.625     ,  0.        ,  0.125     ,  0.25      ,  0.        ],
                       [ 0.125     ,  0.75      ,  0.125     ,  0.        ,  0.        ],
                       [ 0.29166667,  0.        ,  0.625     ,  0.08333333,  0.        ],
                       [ 0.2125    ,  0.        ,  0.125     ,  0.        ,  0.6625    ],
                       [ 0.61111111,  0.        ,  0.16666667,  0.22222222,  0.        ],
                       [ 0.53125   ,  0.125     ,  0.        ,  0.        ,  0.34375   ]];
            }
        }
    }
};
var initialize_arms = function(difficulty, robot_color, condition) {
    // all payoffs and probabilities were randomly generated (with fixed expected rewards across robots)
    // hard coded because javascript can't seed random numbers
    if (robot_color == "Green") {
        if (condition == "observe") {
            if (difficulty == "medium") {
                return [[2,3,4,4], [1,1,0.25,0.5]];
            } else if (difficulty == "hard") {
                return [[3, 3, 1, 3, 4, 1], [1, 0.6666666666666666, 1, 0.6666666666666666, 0.75, 1]];
            }
        } else if (condition == "collaborate") {
            if (difficulty == "easy") {
                return [[3, 2], [0.3333333333333333, 1]];
            } else if (difficulty == "hard") {
                // return [[4,3,4,2,3,3,4,2,4,4], [0.5,1,0.25,0.5,1,1,0.5,1,0.5,0.25]];
                return [[3, 3, 3, 3, 4, 1], [0.3333333333333333, 1, 0.666666666666666, 0.666666666666666, 0.75, 1]];
            }
        }
    } else if (robot_color == "Red") {
        if (condition == "observe") {
            if (difficulty == "medium") {
                return [[3,4,1,2], [1,0.5,1,1]];
            } else if (difficulty == "hard") {
                return [[1, 3, 3, 4, 4, 4], [1, 0.6666666666666666, 0.6666666666666666, 0.75, 0.75, 0.25]];
            }
        } else if (condition == "collaborate") {
            if (difficulty == "easy") {
                return [[2,3], [1,0.3333333333333333]];
            } else if (difficulty == "hard") {
                // return [[4,4,1,2,1,4,4,2,3,4], [0.5,0.75,1,1,1,0.75,0.5,0.5,0.6666666666666666,0.75]];
                return [[4, 3, 4, 4, 3, 3], [0.25, 0.6666666666666666, 0.75, 0.75, 0.6666666666666666, 0.3333333333333333]];
            }
        }
    } else if (robot_color == "Blue") {
        if (condition == "observe") {
            if (difficulty == "medium") {
                return [[3,3,3,3], [0.6666666666666666,1,0.6666666666666666,0.3333333333333333]];
            } else if (difficulty == "hard") {
                return [[3, 4, 3, 3, 2, 4], [0.6666666666666666, 0.75, 0.6666666666666666, 1, 0.5, 0.25]];
            }
        } else if (condition == "collaborate") {
            if (difficulty == "easy") {
                return [[3, 4], [0.3333333333333333,0.5]];
            } else if (difficulty == "hard") {
                // return [[2,4,4,3,4,2,2,3,3,3], [0.5,0.5,0.5,0.3333333333333333,0.75,0.5,1,0.6666666666666666,1,1]];
                return [[4, 4, 3, 3, 3, 4], [0.75, 0.25, 1, 0.6666666666666666, 0.6666666666666666, 0.25]];
            }
        }
    } else if (robot_color == "Yellow") {
        if (condition == "observe") {
            if (difficulty == "medium") {
                return [[3,3,3,2], [0.6666666666666666,1,0.6666666666666666,0.5]];
            } else if (difficulty == "hard") {
                return [[2, 3, 2, 1, 2, 3], [1, 1, 0.5, 1, 1, 1]];
            }
        } else if (condition == "collaborate") {
            if (difficulty == "easy") {
                return [[1, 2], [1, 1]];
            } else if (difficulty == "hard") {
                // return [[3,2,2,2,4,4,2,1,3,3], [1,1,1,0.5,0.75,0.75,1,1,0.3333333333333333,0.6666666666666666]];
                return [[3, 1, 4, 4, 2, 3], [0.3333333333333333, 1, 0.5, 0.75, 1, 1]];
            }
        }
    }
};
var initialize_arms_old = function(difficulty) {
    /*
    Training arms:
        payoffs: [2,3,4,3]
        probabilities: [1,1,0.25,0.6666666666666666]
    Observe Green (medium)
        payoffs: [2,3,4,4]
        probabilities: [1,1,0.25,0.5]
    Collaborate Green (easy)
        payoffs: [3, 2]
        probabilities: [0.3333333333333333, 1]
    Collaborate Green (hard)
        payoffs: [4,3,4,2,3,3,4,2,4,4]
        probabilities: [0.5,1,0.25,0.5,1,1,0.5,1,0.5,0.25]
    Observe Red (medium)
        payoffs: [3,4,1,2]
        probabilities: [1,0.5,1,1]
    Collaborate Red (easy)
        payoffs: [2,3]
        probabilities: [1,0.3333333333333333]
    Collaborate Red (hard)
        payoffs: [4,4,1,2,1,4,4,2,3,4]
        probabilities: [0.5,0.75,1,1,1,0.75,0.5,0.5,0.6666666666666666,0.75]
    Observe Blue (medium)
        payoffs: [3,3,3,3]
        probabilities: [0.6666666666666666,1,0.6666666666666666,0.3333333333333333]
    Collaborate Blue (easy)
        payoffs: [3, 4]
        probabilities: [0.3333333333333333,0.5]
    Collaborate Blue (hard)
        payoffs: [2,4,4,3,4,2,2,3,3,3]
        probabilities: [0.5,0.5,0.5,0.3333333333333333,0.75,0.5,1,0.6666666666666666,1,1]
    Observe Yellow (medium)
        payoffs: [3,3,3,2]
        probabilities: [0.6666666666666666,1,0.6666666666666666,0.5]
    Collaborate Yellow (easy)
        payoffs: [1, 2]
        probabilities: [1, 1]
    Collaborate Yellow (hard)
        payoffs: [3,2,2,2,4,4,2,1,3,3]
        probabilities: [1,1,1,0.5,0.75,0.75,1,1,0.3333333333333333,0.6666666666666666]

    Collab hard (6)
        [[3, 3, 3, 3, 4, 1], [0.3333333333333333, 1, 0.666666666666666, 0.666666666666666, 0.75, 1]]
        [[4, 3, 4, 4, 3, 3], [0.25, 0.6666666666666666, 0.75, 0.75, 0.6666666666666666, 0.3333333333333333]]
        [[4, 4, 3, 3, 3, 4], [0.75, 0.25, 1, 0.6666666666666666, 0.6666666666666666, 0.25]]
        [[3, 1, 4, 4, 2, 3], [0.3333333333333333, 1, 0.5, 0.75, 1, 1]]

    */
    var payoffs_to_sample = [1, 2, 3, 4];
    var payoffs = [];
    var probabilities = [];
    var expected_rewards;
    if (difficulty == "easy") {
        expected_rewards = [1, 2];
        num_arms = 2;
    } else if (difficulty == "hard") {
        // expected_rewards = [1, 1, 1, 2, 2, 2, 2, 3, 3, 3];
        // num_arms = 10;
        expected_rewards = [1, 1, 2, 2, 3, 3];
        num_arms = 6;
    } else {
        expected_rewards = [1, 2, 2, 3];
        num_arms = 4;
    }

    for (i = 0; i < num_arms; i++) {
        idx = Math.floor(Math.random()*expected_rewards.length);
        var done = false;
        while (!done) {
            exp_rew = expected_rewards[idx];
            payoff = payoffs_to_sample[Math.floor(Math.random()*payoffs_to_sample.length)];
            probability = exp_rew / payoff;
            if (probability <= 1) {
                done = true;
            }
        }
        payoffs.push(payoff);
        probabilities.push(probability);
        expected_rewards.splice(idx, 1);
    }
    console.log(payoffs);
    console.log(probabilities);
    return [payoffs, probabilities];
};
var color_arm_values = function(payoffs, probabilities) {
    var num_arms = payoffs.length;
    var colors;
    var colors_worth;
    if (num_arms == 2) {
        colors = colors_easy;
        colors_worth = colors_worth_easy;
    } else if (num_arms == 4) {
        colors = colors_medium;
        colors_worth = colors_worth_medium;
    } else {
        colors = colors_hard;
        colors_worth = colors_worth_hard;
    }
    var expected_rewards = [];
    for (i=0; i < num_arms; i++) {
        expected_rewards.push(payoffs[i] * probabilities[i]);
    }
    for (i=0; i < num_arms; i++) {
        arm = argmax(expected_rewards);
        box = document.getElementById("arm-" + String(arm) + "-value");
        box.style.color = colors[i];
        box.style.backgroundColor = colors[i];
        document.getElementById("arm-" + String(arm) + "-value-text").innerText = colors_worth[i];
        expected_rewards[arm] = -1;
    }
};
var color_arm_values_matrix = function(payoff_matrix) {
    var num_arms = payoff_matrix.length;
    var colors;
    var colors_worth;
    if (num_arms == 2) {
        colors = colors_easy;
        colors_worth = colors_worth_easy;
    } else if (num_arms == 4) {
        colors = colors_medium;
        colors_worth = colors_worth_medium;
    } else {
        colors = colors_hard;
        colors_worth = colors_worth_hard;
    }
    var expected_rewards = [];
    var possible_payoffs = [0, 1, 2, 3, 4];
    for (arm_idx = 0; arm_idx < num_arms; arm_idx++) {
        var probabilities = payoff_matrix[arm_idx];
        var curr_exp_reward = 0;
        for (i = 0; i < probabilities.length; i++) {
            curr_exp_reward += probabilities[i] * possible_payoffs[i];
        }
        expected_rewards.push(curr_exp_reward);
    }
    for (i = 0; i < num_arms; i++) {
        arm = argmax(expected_rewards);
        box = document.getElementById("arm-" + String(arm) + "-value");
        box.style.color = colors[i];
        box.style.backgroundColor = colors[i];
        document.getElementById("arm-" + String(arm) + "-value-text").innerText = colors_worth[i];
        expected_rewards[arm] = -1;
    }
};
var in_range = function(x, num_arms) {
    for (var i = 1; i <= num_arms; i++) {
        if (parseInt(x) == i) {
            return true;
        }
    }
    return false;
};
var prompt_arms = function(num_arms) {
    do {
        var selection = prompt("Which slot do you plan to pick next? [1-" + String(num_arms) + "] Note that this will not actually select the slot.", "");
    } while(selection == null || selection == "" || !in_range(selection, num_arms));
    human_selection = parseInt(selection);
    return selection;
};
var ask_for_decision = function(num_arms) {
    for(var i = 0; i < num_arms; i++) {
        try {
            document.getElementById("arm-" + String(i)).classList.remove(HIGHLIGHT_COLOR);
        } finally {
            document.getElementById("arm-" + String(i)).classList.add(DEFAULT_COLOR);
        }
    };
    window.setTimeout(function() {prompt_arms(num_arms)}, 100);
    return;
};
var sample_arm = function(probabilities) {
    // trust that probabilities sum to 1
    var r = Math.random();
    var low = 0;
    var high = probabilities[0];
    for (i = 0; i < probabilities.length; i++) {
        if (r >= low && r <= high) {
            return i;
        }
        low += probabilities[i];
        if (i == probabilities.length - 1) {
            high = 1;
        } else {
            high += probabilities[i+1];
        }
    }
};

/********************
* HTML manipulation
*
* All HTML files in the templates directory are requested 
* from the server when the PsiTurk object is created above. We
* need code to get those pages from the PsiTurk object and 
* insert them into the document.
*
********************/
var initial_time;

var BetweenConditions = function(next_condition, next_robot_args) {
    psiTurk.showPage('between_conditions.html');
    var num_arms = 6;

    if (next_condition == "observe") {
        $("#message").append("<h2>You will now be <b>observing</b> the Robot " 
            + "in a casino with <b>" + String(num_arms) + "</b> slots.</h2>");
        document.getElementById("observe-instructions").style.display = "block";
    } else if (next_condition == "collaborate") {
        $("#message").append("<h2>You will now be <b>collaborating</b> with the Robot " 
            + "in a casino with <b>" + String(num_arms) + "</b> slots.</h2>");
        document.getElementById("collaborate-instructions").style.display = "block";
    } else if (next_condition == "training") {
        $("#message").append("<h2>You will now be <b>working alone</b> in a casino with "
            + "<b>"+ String(num_arms) + "</b> slots. Remember these slots are different "
            + "than those you've seen before.")
    }
    next = function() {
        var d = new Date();
        initial_time = d.getTime();
        if (next_condition == "observe"){
            currentview = new ObserveRobot(0, 0, next_robot_args);
        } else if (next_condition == "collaborate") {
            currentview = new Collaborate(0, 0, 0, next_robot_args);
        } else if (next_condition == "training") {
            currentview = new PostTraining();
        }
    }
};

var Training = function() {
    psiTurk.showPage('multiarm_bandit.html');

    if (stats == 0 || stats == 1) {
        document.getElementById("prev-reward-text").style.display = "inline";
        document.getElementById("previous-reward").style.display = "inline";
        document.getElementById("prev-arm-text").style.display = "inline";
        document.getElementById("previous-arm").style.display = "inline";
    }

    var num_arms = 6;
    var totalReward = 0;
    var prevReward = 0;
    var averages = new Array(num_arms).fill(0);
    var times_chosen = new Array(num_arms).fill(0);
    var payoff_matrix = [[ 0.2375  ,  0.      ,  0.075   ,  0.      ,  0.6875  ],
                       [ 0.4375  ,  0.125   ,  0.4375  ,  0.      ,  0.      ],
                       [ 0.4375  ,  0.      ,  0.375   ,  0.      ,  0.1875  ],
                       [ 0.75    ,  0.      ,  0.      ,  0.      ,  0.25    ],
                       [ 0.53125 ,  0.      ,  0.4375  ,  0.      ,  0.03125 ],
                       [ 0.484375,  0.1875  ,  0.      ,  0.      ,  0.328125]];
    var iteration = 0;
    var arms_disabled = false;
    var previous_arm_chosen;
    var payoff_history = [...Array(num_arms)].map(e => []);

    // data to be saved
    var all_times_chosen = [];
    var all_average_rewards = [];
    var all_total_rewards = [];
    var all_payoffs = [];
    var all_human_decisions = [];

    var recordData = function(arm, payoff) {
        payoff_history[arm].push(payoff);
        all_times_chosen.push(times_chosen.slice());
        all_average_rewards.push(averages.slice());
        all_total_rewards.push(totalReward);
        all_human_decisions.push(arm);
        all_payoffs.push(payoff);
    }

    clickArm = function(arm_idx) {
        if (arms_disabled) {
            return;
        }
        arms_disabled = true;
        var payoff = sample_arm(payoff_matrix[arm_idx]);

        averages[arm_idx] = ((averages[arm_idx] * times_chosen[arm_idx]) + payoff) / (times_chosen[arm_idx] + 1)
        times_chosen[arm_idx] += 1

        totalReward += payoff;
        prevReward = payoff;
        recordData(arm_idx, payoff);
        iteration += 1;
        previous_arm_chosen = arm_idx + 1;
        
        if (iteration >= NUM_ITERATIONS) {
            finish();
        }

        update();
        window.setTimeout(wait, 300);
    }
    var wait = function() {
        arms_disabled = false;
    }

    var update = function() {
        if (stats == 1) {
            for (i = 0; i < num_arms; i++) {
                average = parseFloat(averages[i]).toFixed(1);
                standard_dev = parseFloat(stddev(payoff_history[i])).toFixed(1);
                disp = String(average) + "±" + String(standard_dev)
                d3.select("#arm-" + String(i) + "-history").text(disp);
            }
        } else if (stats == 2) {
            for (i = 0; i < num_arms; i++) {
                d3.select("#arm-" + String(i) + "-history").text(payoff_history[i].slice(-4));
            }
        }
        d3.select("#reward").text(totalReward);
        d3.select("#previous-arm").text(previous_arm_chosen);
        d3.select("#previous-reward").text(prevReward);
        d3.select("#iteration").text(iteration);
    }

    finish = function() {
        var type = "training";
        var all_data = {'total_reward': totalReward, 'times_chosen': all_times_chosen, 
                        'average_rewards': all_average_rewards, 'human_decisions': all_human_decisions, 
                        'all_total_rewards': all_total_rewards, 'all_payoffs': all_payoffs,
                        'arms_payoff_matrix': payoff_matrix};
        psiTurk.recordUnstructuredData(type, all_data);
        psiTurk.saveData();

        document.getElementById('finish').classList.remove("disabled");
        for (var i = 0; i < num_arms; i++) {
            document.getElementById('arm-' + String(i)).classList.add("disabled");
        }
        document.getElementById('finish').onclick = function() {
            if (mycondition == 0) {
                currentview = new BetweenConditions("observe", {"pretrain": 0, "epsilon": 0.1})
            } else if (mycondition == 1) {
                currentview = new BetweenConditions("collaborate", {"pretrain": 0, "epsilon": 0.1})
            }
        };
    }

    update();
};

var ObserveRobot = function(robot_idx, difficulty_idx, robot_args) {
    var num_arms;
    var difficulty = observation_difficulty_order[difficulty_idx];
    if (difficulty == "easy") {
        psiTurk.showPage('observe_learning_easy.html');
        num_arms = 2;
    } else if (difficulty == "hard") {
        psiTurk.showPage('observe_learning_hard.html');
        num_arms = 6;
    } else {
        psiTurk.showPage('observe_learning.html');
        num_arms = 4;
    }

    if (stats == 0 || stats == 1) {
        document.getElementById("prev-reward-text").style.display = "inline";
        document.getElementById("previous-reward").style.display = "inline";
        document.getElementById("prev-arm-text").style.display = "inline";
        document.getElementById("previous-arm").style.display = "inline";
    }
    document.getElementById("robot-name-text").style.display = "none";
    document.getElementById("robot-name").style.display = "none";

    d3.select("#robot-name").text(robot_colors[robot_idx]);

    var robot_type = robot_order[robot_idx];
    if (robot_type == "random") {
        HIGHLIGHT_COLOR = RANDOM_COLOR;
    } else if (robot_type == "optimal") {
        HIGHLIGHT_COLOR = OPTIMAL_COLOR;
    } else if (robot_type == "greedy") {
        HIGHLIGHT_COLOR = GREEDY_COLOR;
    } else if (robot_type == "greedy2") {
        HIGHLIGHT_COLOR = GREEDY2_COLOR;
    } else if (robot_type == "optimal2") {
        HIGHLIGHT_COLOR = GREEDY2_COLOR;
    }

    casino_name = casino_names[(robot_idx+1)][0];
    d3.select("#casino-name").text("Casino " + casino_name);

    var totalReward = 0;
    var prevReward = 0;
    var averages = new Array(num_arms).fill(0);
    var times_chosen = new Array(num_arms).fill(0);
    console.log(observation_difficulty_order[difficulty_idx], robot_colors[robot_idx])
    var payoff_matrix = initialize_arms_matrix(observation_difficulty_order[difficulty_idx], robot_colors[robot_idx], "observe");
    var iteration = 0;
    var next_idx;
    var to_highlight;
    var click_disabled = false;
    var previous_arm_chosen;
    var finish_task = false;
    var payoff_history = [...Array(num_arms)].map(e => []);
    var gamma = 1; // exploration paramater for modified UCB

    //data to be saved
    var all_times_chosen = [];
    var all_average_rewards = [];
    var all_total_rewards = [];
    var all_payoffs = [];
    var all_robot_decisions = [];

    var chooseNextArm = function() {
        if (robot_type == "random" || robot_type == "greedy" || robot_type == "greedy2") {
            var epsilon = robot_args['epsilon'];
            // console.log(epsilon);
            if (Math.random() > epsilon && iteration != 0) {
                // be greedy, pick argmax
                var all_best = all_argmax(averages);
                var choice = all_best[Math.floor(Math.random()*all_best.length)];
                return [choice, all_best];
            } else {
                // pick randomly
                if (iteration == 0) {
                    // need to manually highlight all arms on iteration 1 bc initialization issues
                    var r = Math.floor(Math.random()*num_arms);
                    return [r, _.range(num_arms)];   
                } else {
                    // highlights all except best arm(s)
                    var all_choices = all_except_argmax(averages);
                    var choice = all_choices[Math.floor(Math.random()*all_choices.length)];
                    return [choice, all_choices];
                }
            }
        } else if (robot_type == "optimal") {
            var avg_plus_conf = [];
            for (var i = 0; i < num_arms; i++) {
                avg_plus_conf.push(averages[i] + Math.sqrt(2 * Math.log(iteration+2) / times_chosen[i]))
            }
            var all_best = all_argmax(avg_plus_conf);
            var choice = all_best[Math.floor(Math.random()*all_best.length)];
            return [choice, all_best];
        } else if (robot_type == "optimal2") {
            var avg_plus_conf = [];
            for (var i = 0; i < num_arms; i++) {
                avg_plus_conf.push(averages[i] + gamma * Math.sqrt(2 * Math.log(iteration+2) / times_chosen[i]))
            }
            gamma = gamma - (1 / 29);
            var all_best = all_argmax(avg_plus_conf);
            var choice = all_best[Math.floor(Math.random()*all_best.length)];
            return [choice, all_best];
        }
    };

    var recordData = function(arm, payoff) {
        payoff_history[arm].push(payoff);
        all_times_chosen.push(times_chosen.slice());
        all_average_rewards.push(averages.slice());
        all_total_rewards.push(totalReward);
        all_payoffs.push(payoff);
        all_robot_decisions.push([arm, to_highlight.slice()]);
    }

    next_iteration = function() {
        if (click_disabled) {
            return;
        }
        document.getElementById("arm-" + String(next_idx)).classList.add("active");
        click_disabled = true;
        previous_arm_chosen = next_idx + 1;
        window.setTimeout(finish_iteration, 1000);
    };

    var finish_iteration = function() {
        document.getElementById("arm-" + String(next_idx)).classList.remove("active");
        unhighlight_arms(to_highlight);

        update();
        var ret = chooseNextArm();
        next_idx = ret[0];
        to_highlight = ret[1];
        highlight_arms(to_highlight);
        click_disabled = false;
    };

    var update = function() {
        var payoff = sample_arm(payoff_matrix[next_idx]);

        averages[next_idx] = ((averages[next_idx] * times_chosen[next_idx]) + payoff) / (times_chosen[next_idx] + 1)
        times_chosen[next_idx] += 1;
        totalReward += payoff;
        prevReward = payoff;
        recordData(next_idx, payoff);
        iteration += 1;
        if (iteration >= NUM_ITERATIONS) {
            finish();
        }
        updateDisplay();
    };

    var updateDisplay = function() {
        if (stats == 1) {
            for (i = 0; i < num_arms; i++) {
                average = parseFloat(averages[i]).toFixed(1);
                standard_dev = parseFloat(stddev(payoff_history[i])).toFixed(1);
                disp = String(average) + "±" + String(standard_dev)
                d3.select("#arm-" + String(i) + "-history").text(disp);
            }
        } else if (stats == 2) {
            for (i = 0; i < num_arms; i++) {
                d3.select("#arm-" + String(i) + "-history").text(payoff_history[i].slice(-4));
            }
        }
        d3.select("#reward").text(totalReward);
        d3.select("#previous-arm").text(previous_arm_chosen);
        d3.select("#previous-reward").text(prevReward);
        d3.select("#iteration").text(iteration);
    };

    finish = function() {
        var type = robot_type + "_" + difficulty + "_observe"
        var all_data = {'robot_type': robot_type, 'difficulty': difficulty, 'robot_args': robot_args, 
                        'total_reward': totalReward, 'times_chosen': all_times_chosen, 
                        'average_rewards': all_average_rewards, 'robot_decisions': all_robot_decisions,
                        'all_total_rewards': all_total_rewards, 'all_payoffs': all_payoffs,
                        'arms_payoff_matrix': payoff_matrix};
        
        // unhighlight_arms([_.range(num_arms)]);
        document.getElementById('next-iteration').onclick = function() {
            psiTurk.recordUnstructuredData(type, all_data);
            currentview = new BetweenConditions("training", {});
        };
        document.getElementById("next-iteration").innerText = "Finish Observing";
    };

    color_arm_values_matrix(payoff_matrix);
    var ret = chooseNextArm();
    next_idx = ret[0];
    to_highlight = ret[1];
    highlight_arms(to_highlight);
    updateDisplay();
};

var Collaborate = function(robot_idx, difficulty_idx, collaboration_idx, robot_args) {
    var collaboration_type = collaboration_order[collaboration_idx];
    var num_arms;
    var difficulty = difficulty_order[difficulty_idx];
    if (difficulty == "easy") {
        psiTurk.showPage('multiarm_bandit_easy.html');
        num_arms = 2;
    } else if (difficulty == "hard") {
        psiTurk.showPage('multiarm_bandit_hard.html');
        num_arms = 6;
    } else {
        psiTurk.showPage('multiarm_bandit.html');
        num_arms = 4;
    }

    if (stats == 0 || stats == 1) {
        document.getElementById("prev-reward-text").style.display = "inline";
        document.getElementById("previous-reward").style.display = "inline";
        document.getElementById("prev-arm-text").style.display = "inline";
        document.getElementById("previous-arm").style.display = "inline";
    }

    document.getElementById("robot-name-text").style.display = "none";
    document.getElementById("robot-name").style.display = "none";
    d3.select("#robot-name").text(robot_colors[robot_idx]);

    var robot_type = robot_order[robot_idx];
    if (robot_type == "random") {
        HIGHLIGHT_COLOR = RANDOM_COLOR;
    } else if (robot_type == "optimal") {
        HIGHLIGHT_COLOR = OPTIMAL_COLOR;
    } else if (robot_type == "greedy") {
        HIGHLIGHT_COLOR = GREEDY_COLOR;
    } else if (robot_type == "greedy2") {
        HIGHLIGHT_COLOR = GREEDY2_COLOR;
    } else if (robot_type == "optimal2") {
        HIGHLIGHT_COLOR = GREEDY2_COLOR;
    }

    casino_name = casino_names[(robot_idx+1)][1];
    d3.select("#casino-name").text("Casino " + casino_name);

    var totalReward = 0;
    var prevReward = 0;
    var averages = new Array(num_arms).fill(0);
    var times_chosen = new Array(num_arms).fill(0);
    var payoff_matrix = initialize_arms_matrix(difficulty_order[difficulty_idx], robot_colors[robot_idx], "collaborate");
    var iteration = 0;
    var next_idx;
    var to_highlight = _.range(num_arms);
    var next_disabled = false;
    var arms_disabled = false;
    var turn = "robot";
    var previous_arm_chosen;
    var pretrain_averages = [];
    var payoff_history = [...Array(num_arms)].map(e => []);
    var gamma = 1; // exploration parameter for modified UCB

    //data to be recorded
    var all_times_chosen = [];
    var all_average_rewards = [];
    var all_total_rewards = [];
    var all_payoffs = [];
    var all_human_decisions = [];
    var all_before_suggest_decisions = [];
    var all_robot_decisions = [];
    var all_pretrain_decisions = [];
    var all_pretrain_rewards = [];

    var chooseNextArm = function() {
        // return value [r, [r1, r2,...]] in form [forced selection, all equal arms to highlight]

        // if (collaboration_type == "suggest" && iteration >= robot_args['pretrain']) {
        //  r = argmax(pretrain_averages);
        //  return [r, [r]];
        // }
        if (robot_type == "random" || robot_type == "greedy" || robot_type == "greedy2") {
            var epsilon = robot_args['epsilon'];
            if (Math.random() > epsilon && iteration != 0) {
                // be greedy, pick argmax
                var all_best = all_argmax(averages);
                var choice = all_best[Math.floor(Math.random()*all_best.length)];
                return [choice, all_best];
            } else {
                // pick randomly
                if (iteration == 0) {
                    var r = Math.floor(Math.random()*num_arms);
                    return [r, _.range(num_arms)];   
                } else {
                    // var r = Math.floor(Math.random()*num_arms);
                    var all_choices = all_except_argmax(averages);
                    var choice = all_choices[Math.floor(Math.random()*all_choices.length)];
                    return [choice, all_choices];
                }
            }
        } else if (robot_type == "optimal") {
            var avg_plus_conf = [];
            for (var i = 0; i < num_arms; i++) {
                avg_plus_conf.push(averages[i] + Math.sqrt(2 * Math.log(iteration+2) / times_chosen[i]))
            }
            var all_best = all_argmax(avg_plus_conf);
            var choice = all_best[Math.floor(Math.random()*all_best.length)];
            return [choice, all_best];
        } else if (robot_type == "optimal2") {
            var avg_plus_conf = [];
            for (var i = 0; i < num_arms; i++) {
                avg_plus_conf.push(averages[i] + gamma * Math.sqrt(2 * Math.log(iteration+2) / times_chosen[i]))
            }
            gamma = gamma - (1 / 29);
            var all_best = all_argmax(avg_plus_conf);
            var choice = all_best[Math.floor(Math.random()*all_best.length)];
            return [choice, all_best];
        }
    };

    var recordData = function(arm, payoff) {
        payoff_history[arm].push(payoff);
        all_times_chosen.push(times_chosen.slice());
        all_average_rewards.push(averages.slice());
        all_total_rewards.push(totalReward);
        all_payoffs.push(payoff);
        if (collaboration_type == "suggest") {
            all_robot_decisions.push(to_highlight.slice());
            all_human_decisions.push(arm);
        } else if (collaboration_type == "turns") {
            if (turn == "robot") {
                all_robot_decisions.push(arm);
                all_human_decisions.push(-1);
            } else if (turn == "human") {
                all_robot_decisions.push(-1);
                all_human_decisions.push(arm);
            }
        }
    }
    var recordPretrainData = function(arm, payoff) {
        all_pretrain_decisions.push(arm);
        all_pretrain_rewards.push(payoff);
    }

    clickArm = function(arm_idx, robot_click = false) {
        if (arms_disabled && !robot_click) {
            return;
        }
        all_before_suggest_decisions.push(human_selection);
        arms_disabled = true;
        unhighlight_arms(to_highlight);
        var payoff = sample_arm(payoff_matrix[arm_idx]);

        averages[arm_idx] = ((averages[arm_idx] * times_chosen[arm_idx]) + payoff) / (times_chosen[arm_idx] + 1)
        times_chosen[arm_idx] += 1

        totalReward += payoff;
        prevReward = payoff;
        recordData(arm_idx, payoff);
        iteration += 1;
        previous_arm_chosen = arm_idx + 1;
        
        if (iteration >= NUM_ITERATIONS + robot_args["pretrain"]) {
            update();
            finish();
            return;
        }

        update();
        var ret = chooseNextArm();
        next_idx = ret[0];
        to_highlight = ret[1];
        // highlight_arms(to_highlight);
        window.setTimeout(wait, 100);
        return;
    };

    var wait = function() {
        arms_disabled = false;
        ask_for_decision(num_arms);
        window.setTimeout(function() {highlight_arms(to_highlight)}, 400);
        return;
    }

    var pretrain = function(arm_idx) {
        if (arms_disabled) {
            return;
        }
        var payoff = sample_arm(payoff_matrix[arm_idx]);

        averages[arm_idx] = ((averages[arm_idx] * times_chosen[arm_idx]) + payoff) / (times_chosen[arm_idx] + 1)
        times_chosen[arm_idx] += 1
        recordPretrainData(arm_idx, payoff);

        iteration += 1;
        var ret = chooseNextArm();
        next_idx = ret[0];
    }

    next_iteration = function() {
        if (next_disabled) {
            return;
        }
        document.getElementById("arm-" + String(next_idx)).classList.add("active");
        next_disabled = true;
        arms_disabled = true;
        window.setTimeout(finish_iteration, 1000);
    };

    var finish_iteration = function() {
        clickArm(next_idx, true);
        document.getElementById("arm-" + String(next_idx)).classList.remove("active");
        unhighlight_arms(to_highlight);

        // update();
    };

    var update = function() {
        if (stats == 1) {
            for (i = 0; i < num_arms; i++) {
                average = parseFloat(averages[i]).toFixed(1);
                standard_dev = parseFloat(stddev(payoff_history[i])).toFixed(1);
                disp = String(average) + "±" + String(standard_dev)
                d3.select("#arm-" + String(i) + "-history").text(disp);
            }
        } else if (stats == 2) {
            for (i = 0; i < num_arms; i++) {
                d3.select("#arm-" + String(i) + "-history").text(payoff_history[i].slice(-4));
            }
        }
        d3.select("#reward").text(totalReward);
        d3.select("#previous-arm").text(previous_arm_chosen);
        d3.select("#previous-reward").text(prevReward);
        d3.select("#iteration").text(iteration - robot_args["pretrain"]);
        if (collaboration_type == "turns" && turn == "human") {
            turn = "robot";
            $("#reward").append("<p></p><h1 style='display: inline' id='turn'>Turn: Robot</h1>")
            $("#turn").append("<div class='row'><button type='button' id='next-iteration' class='btn btn-primary btn-lg' onclick='next_iteration()'> Next <span class='glyphicon glyphicon-arrow-right'></button></div>")
            next_disabled = false;
            arms_disabled = true;
        } else if (collaboration_type == "turns" && turn == "robot") {
            turn = "human";
            $("#reward").append("<p></p><h1 style='display: inline' id='turn'>Turn: Human</h1>")
            $("#turn").append("<div class='row'><button type='button' id='next-iteration' class='btn btn-primary btn-lg disabled' onclick='next_iteration()'> Next <span class='glyphicon glyphicon-arrow-right'></button></div>")
            next_disabled = true;
            arms_disabled = false;
        }
    };

    var first_iteration = function() {
        if (collaboration_type == "suggest") {
            var ret = chooseNextArm();
            next_idx = ret[0];
            to_highlight = ret[1];
            highlight_arms(to_highlight);
        }
        return;
    }

    finish = function() {
        var type = robot_type + "_" + difficulty + "_collaborate_" + collaboration_type
        var all_data = {'robot_type': robot_type, 'difficulty': difficulty, 'robot_args': robot_args, 
                    'collaboration_type': collaboration_type, 'total_reward': totalReward,
                    'times_chosen': all_times_chosen, 'average_rewards': all_average_rewards, 
                    'human_decisions': all_human_decisions, 'robot_decisions': all_robot_decisions,
                    'all_total_rewards': all_total_rewards, 'all_payoffs': all_payoffs,
                    'arms_payoff_matrix': payoff_matrix,
                    'pretrain_decisions': all_pretrain_decisions, 'pretrain_payoffs': all_pretrain_rewards,
                    'before_suggest_decisions': all_before_suggest_decisions};
        // psiTurk.recordUnstructuredData(type, all_data);
        // psiTurk.saveData();

        arms_disabled = true;
        document.getElementById('finish').classList.remove("disabled");
        for (var i = 0; i < num_arms; i++) {
            document.getElementById('arm-' + String(i)).classList.add("disabled");
        }
        document.getElementById('finish').onclick = function() {
            psiTurk.recordUnstructuredData(type, all_data);
            currentview = new BetweenConditions("training", {});
        };
    };

    // Pretrain robot
    for (var i = 0; i < robot_args["pretrain"]; i++) {
        to_highlight = [];
        var ret = chooseNextArm();
        pretrain(ret[0]);
    }
    pretrain_averages = averages.slice();
    // reset variables, iteration number necessary for math to work
    totalReward = 0;
    prevReward = 0;

    unhighlight_arms(_.range(num_arms));
    update();
    ask_for_decision(num_arms);
    window.setTimeout(first_iteration, 100);
};

var PostTraining = function() {
    psiTurk.showPage('multiarm_bandit.html');

    if (stats == 0 || stats == 1) {
        document.getElementById("prev-reward-text").style.display = "inline";
        document.getElementById("previous-reward").style.display = "inline";
        document.getElementById("prev-arm-text").style.display = "inline";
        document.getElementById("previous-arm").style.display = "inline";
    }
    d3.select("#finish").text("Finish")
    d3.select("#casino-name").text("Casino C");

    var num_arms = 6;
    var totalReward = 0;
    var prevReward = 0;
    var averages = new Array(num_arms).fill(0);
    var times_chosen = new Array(num_arms).fill(0);
    var payoff_matrix = [[ 0.53125 ,  0.      ,  0.4375  ,  0.      ,  0.03125 ],
                       [ 0.75    ,  0.      ,  0.      ,  0.      ,  0.25    ],
                       [ 0.2375  ,  0.      ,  0.075   ,  0.      ,  0.6875  ],
                       [ 0.4375  ,  0.      ,  0.375   ,  0.      ,  0.1875  ],
                       [ 0.484375,  0.1875  ,  0.      ,  0.      ,  0.328125],
                       [ 0.4375  ,  0.125   ,  0.4375  ,  0.      ,  0.      ]];
    var iteration = 0;
    var arms_disabled = false;
    var previous_arm_chosen;
    var payoff_history = [...Array(num_arms)].map(e => []);

    // data to be saved
    var all_times_chosen = [];
    var all_average_rewards = [];
    var all_total_rewards = [];
    var all_payoffs = [];
    var all_human_decisions = [];

    var recordData = function(arm, payoff) {
        payoff_history[arm].push(payoff);
        all_times_chosen.push(times_chosen.slice());
        all_average_rewards.push(averages.slice());
        all_total_rewards.push(totalReward);
        all_human_decisions.push(arm);
        all_payoffs.push(payoff);
    }

    clickArm = function(arm_idx) {
        if (arms_disabled) {
            return;
        }
        arms_disabled = true;
        var payoff = sample_arm(payoff_matrix[arm_idx]);

        averages[arm_idx] = ((averages[arm_idx] * times_chosen[arm_idx]) + payoff) / (times_chosen[arm_idx] + 1)
        times_chosen[arm_idx] += 1

        totalReward += payoff;
        prevReward = payoff;
        recordData(arm_idx, payoff);
        iteration += 1;
        previous_arm_chosen = arm_idx + 1;
        
        if (iteration >= NUM_ITERATIONS) {
            finish();
        }

        update();
        window.setTimeout(wait, 300);
    }
    var wait = function() {
        arms_disabled = false;
    }

    var update = function() {
        if (stats == 1) {
            for (i = 0; i < num_arms; i++) {
                average = parseFloat(averages[i]).toFixed(1);
                standard_dev = parseFloat(stddev(payoff_history[i])).toFixed(1);
                disp = String(average) + "±" + String(standard_dev)
                d3.select("#arm-" + String(i) + "-history").text(disp);
            }
        } else if (stats == 2) {
            for (i = 0; i < num_arms; i++) {
                d3.select("#arm-" + String(i) + "-history").text(payoff_history[i].slice(-4));
            }
        }
        d3.select("#reward").text(totalReward);
        d3.select("#previous-arm").text(previous_arm_chosen);
        d3.select("#previous-reward").text(prevReward);
        d3.select("#iteration").text(iteration);
    }

    finish = function() {
        var type = "post_training";
        var all_data = {'total_reward': totalReward, 'times_chosen': all_times_chosen, 
                        'average_rewards': all_average_rewards, 'human_decisions': all_human_decisions, 
                        'all_total_rewards': all_total_rewards, 'all_payoffs': all_payoffs,
                        'arms_payoff_matrix': payoff_matrix};
        psiTurk.recordUnstructuredData(type, all_data);
        psiTurk.saveData();

        document.getElementById('finish').classList.remove("disabled");
        for (var i = 0; i < num_arms; i++) {
            document.getElementById('arm-' + String(i)).classList.add("disabled");
        }
        document.getElementById('finish').onclick = function() {
            currentview = new FinalQuestionnaire();
        };
    }

    update();
};

var FinalQuestionnaire = function() {
    psiTurk.showPage('testing_questionnaire.html');

    finish = function() {
        var gender = document.querySelector('input[name="gender"]:checked').value;
        var age = document.getElementById("age").value;
        var comments = document.getElementById("comments").value;
        psiTurk.recordUnstructuredData("gender", gender);
        psiTurk.recordUnstructuredData("age", age);
        psiTurk.recordUnstructuredData("robot_order", robot_order.slice());
        psiTurk.recordUnstructuredData("robot_colors", robot_colors.slice());
        psiTurk.recordUnstructuredData("observation_difficulty_order", observation_difficulty_order.slice());
        psiTurk.recordUnstructuredData("collaborate_difficulty_order", difficulty_order.slice());
        psiTurk.recordUnstructuredData("comments", comments);
        psiTurk.recordUnstructuredData("num_iterations", NUM_ITERATIONS);
        psiTurk.saveData({
            success: function() {
                psiTurk.completeHIT();
            }
        });
    }
};

// Task object to keep track of the current phase
var currentview;

/*******************
 * Run Task
 ******************/
$(window).load( function(){
    psiTurk.doInstructions(
        instructionPages, // a list of pages you want to display in sequence
        function() { 
            currentview = new Training();
        }
    );
});
