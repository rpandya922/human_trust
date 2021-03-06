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
// const EXPERIMENT_TYPE = "stats"; // MAKE SURE TO SET num_conds = 4 in config.txt
const EXPERIMENT_TYPE = "observe"; // MAKE SURE TO SET num_conds = 2 in config.txt
// collaborate only mode
mycondition = 1;
// showing previous 4 mode
stats = -1;
////////////////////////////////////////////////////////////////////////////////////////////////////////

var pages = [
    "instructions/human_only_instructions.html",
    "multiarm_bandit.html",
    "multiarm_bandit_easy.html",
    "multiarm_bandit_hard.html",
    "observe_learning.html",
    "observe_learning_easy.html",
    "observe_learning_hard.html",
    "between_conditions.html", 
    "postquestionnaire.html",
    "robot_question.html",
    "human_only_questions.html"
];

psiTurk.preloadPages(pages);

var instructionPages = [ // add as a list as many pages as you like
    "instructions/human_only_instructions.html"
];

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
var robot_order = match_shuffle(["greedy", "optimal2", "optimal", "random"], robot_shuffle_order);
var robot_colors = match_shuffle(["Green", "Red", "Blue", "Yellow"], robot_shuffle_order);
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
var BetweenConditions = function(next_robot_idx, next_diff_idx, next_robot_args, next_condition) {
    psiTurk.showPage('between_conditions.html');
    var num_arms = 6;
    $("#message").append("<h2>You will now work in a different casino with <b>" + String(num_arms) + "</b> slots.</h2> " + 
        "You will have <b>30 Turns.</b> Click Next to begin.");
    next = function() {
        var d = new Date();
        initial_time = d.getTime();
        currentview = new Testing();
    }
};

var Training = function() {
    psiTurk.showPage('multiarm_bandit.html');

    if (stats == 0 || stats == 1 || stats == 2 || stats == 3) {
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
    // var payoff_matrix = [[ 0.2375  ,  0.      ,  0.075   ,  0.      ,  0.6875  ],
    //                    [ 0.4375  ,  0.125   ,  0.4375  ,  0.      ,  0.      ],
    //                    [ 0.4375  ,  0.      ,  0.375   ,  0.      ,  0.1875  ],
    //                    [ 0.75    ,  0.      ,  0.      ,  0.      ,  0.25    ],
    //                    [ 0.53125 ,  0.      ,  0.4375  ,  0.      ,  0.03125 ],
    //                    [ 0.484375,  0.1875  ,  0.      ,  0.      ,  0.328125]];
    payoff_matrix = [[ 0.16666667,  0.75      ,  0.        ,  0.08333333,  0.        ],
                   [ 0.5625    ,  0.        ,  0.375     ,  0.        ,  0.0625    ],
                   [ 0.53125   ,  0.125     ,  0.        ,  0.        ,  0.34375   ],
                   [ 0.703125  ,  0.        ,  0.        ,  0.1875    ,  0.109375  ],
                   [ 0.36111111,  0.        ,  0.41666667,  0.22222222,  0.        ],
                   [ 0.0875    ,  0.25      ,  0.        ,  0.        ,  0.6625    ]];
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
            // Show mean only
            for (i = 0; i < num_arms; i++) {
                average = parseFloat(averages[i]).toFixed(1);
                disp = String(average)
                d3.select("#arm-" + String(i) + "-history").text(disp);
            }
        } else if (stats == 2) {
            // Show number of times pulled
            for (i = 0; i < num_arms; i++) {
                disp = String(payoff_history[i].length)
                d3.select("#arm-" + String(i) + "-history").text(disp);
            }
        } else if (stats == 3) {
            // Show mean + num pulls
            for (i = 0; i < num_arms; i++) {
                average = parseFloat(averages[i]).toFixed(1);
                num_pulls = payoff_history[i].length
                disp = String(average) + ", " + String(num_pulls)
                d3.select("#arm-" + String(i) + "-history").text(disp);
            }
        } else if (stats == -1) {
            // for original study: show previous 4 pulls
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
            currentview = new BetweenConditions(0, 0, {"pretrain": 0, "epsilon": 0.1}, "observe");
        };
    }

    update();
};

var Testing = function() {
    psiTurk.showPage('multiarm_bandit.html');

    if (stats == 0 || stats == 1 || stats == 2 || stats == 3) {
        document.getElementById("prev-reward-text").style.display = "inline";
        document.getElementById("previous-reward").style.display = "inline";
        document.getElementById("prev-arm-text").style.display = "inline";
        document.getElementById("previous-arm").style.display = "inline";
    }

    d3.select("#casino-name").text("Casino B");

    var num_arms = 6;
    var totalReward = 0;
    var prevReward = 0;
    var averages = new Array(num_arms).fill(0);
    var times_chosen = new Array(num_arms).fill(0);
    // var payoff_matrix = [[ 0.2375  ,  0.      ,  0.075   ,  0.      ,  0.6875  ],
    //                    [ 0.4375  ,  0.125   ,  0.4375  ,  0.      ,  0.      ],
    //                    [ 0.4375  ,  0.      ,  0.375   ,  0.      ,  0.1875  ],
    //                    [ 0.75    ,  0.      ,  0.      ,  0.      ,  0.25    ],
    //                    [ 0.53125 ,  0.      ,  0.4375  ,  0.      ,  0.03125 ],
    //                    [ 0.484375,  0.1875  ,  0.      ,  0.      ,  0.328125]];
    payoff_matrix = [[ 0.16666667,  0.75      ,  0.        ,  0.08333333,  0.        ],
                   [ 0.25      ,  0.5       ,  0.        ,  0.        ,  0.25      ],
                   [ 0.09375   ,  0.875     ,  0.        ,  0.        ,  0.03125   ],
                   [ 0.228125  ,  0.0625    ,  0.        ,  0.        ,  0.709375  ],
                   [ 0.54166667,  0.        ,  0.        ,  0.33333333,  0.125     ],
                   [ 0.5       ,  0.        ,  0.5       ,  0.        ,  0.        ]];
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
            // Show mean only
            for (i = 0; i < num_arms; i++) {
                average = parseFloat(averages[i]).toFixed(1);
                disp = String(average)
                d3.select("#arm-" + String(i) + "-history").text(disp);
            }
        } else if (stats == 2) {
            // Show number of times pulled
            for (i = 0; i < num_arms; i++) {
                disp = String(payoff_history[i].length)
                d3.select("#arm-" + String(i) + "-history").text(disp);
            }
        } else if (stats == 3) {
            // Show mean + num pulls
            for (i = 0; i < num_arms; i++) {
                average = parseFloat(averages[i]).toFixed(1);
                num_pulls = payoff_history[i].length
                disp = String(average) + ", " + String(num_pulls)
                d3.select("#arm-" + String(i) + "-history").text(disp);
            }
        } else if (stats == -1) {
            // for original study: show previous 4 pulls
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
        var type = "testing";
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
    psiTurk.showPage('human_only_questions.html');

    finish = function() {
        var gender = document.querySelector('input[name="gender"]:checked').value;
        var age = document.getElementById("age").value;
        var comments = document.getElementById("comments").value;
        psiTurk.recordUnstructuredData("gender", gender);
        psiTurk.recordUnstructuredData("age", age);
        psiTurk.recordUnstructuredData("comments", comments);
        psiTurk.recordUnstructuredData("num_iterations", NUM_ITERATIONS);
        psiTurk.saveData({
            success: function() {
                psiTurk.completeHIT();
            }
        });
    }
};

var Questionnaire = function(prev_robot_idx, next_robot_idx, next_diff_idx, next_robot_args, next_condition, final_robot = false) {
    psiTurk.showPage('robot_question.html');
    var robot = robot_colors[prev_robot_idx];
    document.getElementById('robot-name').innerText = robot;
    finish = function() {
        var d = new Date();
        var final_time = d.getTime();
        var time_taken = final_time - initial_time;
        var trust = document.querySelector('input[name="robot-trust"]:checked').value;
        var useful = document.querySelector('input[name="robot-useful"]:checked').value;
        var advice = document.querySelector('input[name="robot-advice"]:checked').value;
        psiTurk.recordUnstructuredData("trust_robot_" + String(robot), trust);
        psiTurk.recordUnstructuredData("useful_robot_" + String(robot), useful);
        psiTurk.recordUnstructuredData("advice_robot_" + String(robot), advice);
        psiTurk.recordUnstructuredData("time_taken_" + String(robot), time_taken);
        if (EXPERIMENT_TYPE == "stats") {
            psiTurk.recordUnstructuredData("condition", stats);
        } else if (EXPERIMENT_TYPE == "observe") {
            psiTurk.recordUnstructuredData("condition", mycondition);
        }
        psiTurk.saveData();
        if (final_robot) {
            currentview = new FinalQuestionnaire();
            return; 
        } else {
            currentview = new BetweenConditions(next_robot_idx, next_diff_idx, next_robot_args, next_condition);
        }
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
