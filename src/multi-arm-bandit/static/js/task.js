/*
 * Requires:
 *     psiturk.js
 *     utils.js
 */

// Initalize psiturk object
var psiTurk = new PsiTurk(uniqueId, adServerLoc, mode);

var mycondition = condition;  // these two variables are passed by the psiturk server process
var mycounterbalance = counterbalance;  // they tell you which condition you have been assigned to
// they are not used in the stroop code but may be useful to you

// All pages to be loaded
var pages = [
	"instructions/instruct-1.html",
	"multiarm_bandit.html",
	"multiarm_bandit_easy.html",
	"multiarm_bandit_hard.html",
	"observe_learning.html",
	"observe_learning_easy.html",
	"observe_learning_hard.html",
	"between_conditions.html", 
	"postquestionnaire.html"
];

psiTurk.preloadPages(pages);

var instructionPages = [ // add as a list as many pages as you like
	"instructions/instruct-1.html",
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
const NUM_ITERATIONS = 5;

//Make sure color and order are shuffled the same way
var robot_order = ["greedy", "greedy2", "optimal", "random"];
var robot_colors = ["Green", "Red", "Blue", "Yellow"];
var difficulty_order = ["easy", "hard"];
var collaboration_order = ["suggest", "turns"];
var colors_easy = ["#16BF00", "#E5001E"];
// var colors_hard = ["#16BF00", "#43C300", "#71C700", "#A1CB00", "#CFCC00",
// 			  	   "#D4A100", "#D87400", "#DC4500", "#E01400", "#E5001E"];
var colors_hard = ["#16BF00", "#16BF00", "#16BF00", "#D2B800", "#D2B800",
			  	   "#D2B800", "#D2B800", "#E5001E", "#E5001E", "#E5001E"];

function shuffle(a) {
    for (let i = a.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [a[i], a[j]] = [a[j], a[i]];
    }
    return a;
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

var initialize_arms = function(difficulty) {
	var payoffs_to_sample = [1, 2, 3, 4];
	var payoffs = [];
	var probabilities = [];
	var expected_rewards;
	if (difficulty == "easy") {
		expected_rewards = [1, 2];
		num_arms = 2;
	} else if (difficulty == "hard") {
		expected_rewards = [1, 1, 1, 2, 2, 2, 2, 3, 3, 3];
		num_arms = 10;
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
}

var color_arm_values = function(payoffs, probabilities) {
	var num_arms = payoffs.length;
	var colors;
	if (num_arms <= 5) {
		colors = colors_easy;
	} else {
		colors = colors_hard;
	}
	var expected_rewards = [];
	for (i=0; i < num_arms; i++) {
		expected_rewards.push(payoffs[i] * probabilities[i]);
	}
	for (i=0; i < num_arms; i++) {
		arm = argmax(expected_rewards);
		box = document.getElementById("arm-" + String(arm) + "-value")
		box.style.color = colors[i];
		box.style.backgroundColor = colors[i];
		expected_rewards[arm] = -1;
	}
}

/********************
* HTML manipulation
*
* All HTML files in the templates directory are requested 
* from the server when the PsiTurk object is created above. We
* need code to get those pages from the PsiTurk object and 
* insert them into the document.
*
********************/

var BetweenConditions = function(next_robot_idx, next_diff_idx, next_robot_args, next_condition) {
	psiTurk.showPage('between_conditions.html');
	var num_arms;
	if (difficulty_order[next_diff_idx] == "easy") {
		num_arms = 2;
	} else if (difficulty_order[next_diff_idx] == "hard") {
		num_arms = 10;
	} else {
		num_arms = 4;
	}
	if (robot_order[next_robot_idx] == "greedy2") {
		next_robot_args['epsilon'] = 0.3;
	} else {
		next_robot_args['epsilon'] = 0.1;
	}
	var color = robot_colors[next_robot_idx];
	if (next_condition == "observe") {
		$("#message").append("<h2>You will now be <b>observing</b> the <b><em>" + color + " Robot" 
			+ "</em></b> on a task with <b>" + String(num_arms) + "</b> arms.</h2>");
		document.getElementById("observe-instructions").style.display = "block";
	} else if (next_condition == "collaborate") {
		$("#message").append("<h2>You will now be <b>collaborating</b> with the <b><em>" + color + " Robot" 
			+ "</em></b> on a task with <b>" + String(num_arms) + "</b> arms.</h2>");
		document.getElementById("collaborate-instructions").style.display = "block";
	}
	next = function() {
		if (next_condition == "observe"){
			currentview = new ObserveRobot(next_robot_idx, next_diff_idx, next_robot_args);
		} else if (next_condition == "collaborate") {
			currentview = new Collaborate(next_robot_idx, next_diff_idx, 0, next_robot_args);
			// currentview = new Collaborate(0, 0, 0, next_robot_args);
		}
	}
};

var Training = function() {
	psiTurk.showPage('multiarm_bandit.html');

	var num_arms = 4;
	var totalReward = 0;
	var prevReward = 0;
	var averages = new Array(num_arms).fill(0);
	var times_chosen = new Array(num_arms).fill(0);
	var payoffs = _.range(num_arms);
	var probabilities = new Array(num_arms).fill(1);
	var iteration = 0;
	var arms_disabled = false;
	var previous_arm_chosen;

	clickArm = function(arm_idx) {
		if (arms_disabled) {
			return;
		}
		arms_disabled = true;
		var r = Math.random();
		var payoff = 0;
		if (r < probabilities[arm_idx]) {
			payoff = payoffs[arm_idx];
		}

		averages[arm_idx] = ((averages[arm_idx] * times_chosen[arm_idx]) + payoff) / (times_chosen[arm_idx] + 1)
		times_chosen[arm_idx] += 1

		totalReward += payoff;
		prevReward = payoff;
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
		d3.select("#reward").text(totalReward);
		d3.select("#previous-arm").text(previous_arm_chosen);
		d3.select("#previous-reward").text(prevReward);
		d3.select("#iteration").text(iteration);
	}

	finish = function() {
		currentview = new BetweenConditions(0, 0, {"pretrain": 100, "epsilon": 0.1}, "observe");
	}

	update();
};

var BetweenConditionsCollab = function(next_robot_idx, next_diff_idx, next_collab_idx, next_robot_args) {
	psiTurk.showPage('between_conditions.html');
	var num_arms;
	if (difficulty_order[next_diff_idx] == "easy") {
		num_arms = 2;
	} else if (difficulty_order[next_diff_idx] == "hard") {
		num_arms = 10;
	} else {
		num_arms = 4;
	}
	var color = robot_colors[next_robot_idx];
	$("#message").append("<h2>You will now be <em>collaborating</em> with the <b><em>" + color + " Robot" 
			+ "</em></b> on a task with <b>" + String(num_arms) + "</b> arms.</h2>");
	next = function() {
		currentview = new Collaborate(next_robot_idx, next_diff_idx, next_collab_idx, next_robot_args);
	}
};

var ObserveRobot = function(robot_idx, difficulty_idx, robot_args) {
	var num_arms;
	var difficulty = difficulty_order[difficulty_idx];
	if (difficulty == "easy") {
		psiTurk.showPage('observe_learning_easy.html');
		num_arms = 2;
	} else if (difficulty == "hard") {
		psiTurk.showPage('observe_learning_hard.html');
		num_arms = 10;
	} else {
		psiTurk.showPage('observe_learning.html');
		num_arms = 4;
	}
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
	}
	console.log(robot_args['epsilon']);

	// const num_arms = 4;
	var totalReward = 0;
	var prevReward = 0;
	var averages = new Array(num_arms).fill(0);
	var times_chosen = new Array(num_arms).fill(0);
	let [payoffs, probabilities] = initialize_arms(difficulty_order[difficulty_idx]);
	var iteration = 0;
	var next_idx;
	var to_highlight;
	var click_disabled = false;
	var previous_arm_chosen;
	var finish_task = false;

	//data to be saved
	var all_times_chosen = [];
	var all_average_rewards = [];
	var all_total_rewards = [];
	var all_robot_decisions = [];

	var chooseNextArm = function() {
		if (robot_type == "random") {
			var r = Math.floor(Math.random()*num_arms);
			// first element for arm to pull
			// second array is for which arms to highlight, in case of multiple
			return [r, [r]];
		} else if (robot_type == "greedy" || robot_type == "greedy2") {
			var epsilon = robot_args['epsilon'];
			if (Math.random() > epsilon && iteration != 0) {
				// be greedy, pick argmax
				var r = argmax(averages);
				return [r, [r]];
			} else {
				// pick randomly
				var r = Math.floor(Math.random()*num_arms);
				return [r, _.range(num_arms)];
			}
		} else if (robot_type == "optimal") {
			if (iteration < num_arms) {
				// pick each arm once to begin
				return [iteration, [iteration]];
			}
			var avg_plus_conf = [];
			for (var i = 0; i < num_arms; i++) {
				avg_plus_conf.push(averages[i] + Math.sqrt(2 * Math.log(iteration) / times_chosen[i]))
			}
			var r = argmax(avg_plus_conf);
			return [r, [r]];
		}
	};

	var recordData = function(arm) {
		all_times_chosen.push(times_chosen.slice());
		all_average_rewards.push(averages.slice());
		all_total_rewards.push(totalReward);
		all_robot_decisions.push(arm);
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
		times_chosen[next_idx] += 1;
		click_disabled = false;
	};

	var update = function() {
		var r = Math.random();
		var payoff = 0;
		if (r < probabilities[next_idx]) {
			payoff = payoffs[next_idx];
		}

		averages[next_idx] = ((averages[next_idx] * times_chosen[next_idx]) + payoff) / (times_chosen[next_idx] + 1)

		totalReward += payoff;
		prevReward = payoff;
		recordData(next_idx);
		iteration += 1;
		if (iteration >= NUM_ITERATIONS) {
			finish();
		}
		updateDisplay();
	};

	var updateDisplay = function() {
		d3.select("#reward").text(totalReward);
		d3.select("#previous-arm").text(previous_arm_chosen);
		d3.select("#previous-reward").text(prevReward);
		d3.select("#iteration").text(iteration);
	};

	finish = function() {
		type = robot_type + "_" + difficulty + "_observe"
		all_data = {'robot_type': robot_type, 'difficulty': difficulty, 'robot_args': robot_args, 
					'total_reward': totalReward, 'times_chosen': all_times_chosen, 
					'average_rewards': all_average_rewards, 'robot_decisions': all_robot_decisions,
					'all_rewards': all_total_rewards, 'arm_payoffs': payoffs, 'arm_probabilities': probabilities};
		psiTurk.saveData();
		
		// unhighlight_arms([_.range(num_arms)]);
		document.getElementById('next-iteration').onclick = function() {
			if (difficulty_idx == difficulty_order.length - 1) {
				currentview = new BetweenConditions(robot_idx, 0, robot_args, "collaborate");
			} else {
				currentview = new BetweenConditions(robot_idx, difficulty_idx + 1, robot_args, "observe");
			}
		};
		document.getElementById("next-iteration").innerText = "Finish Observing";

		// if (difficulty_idx == difficulty_order.length - 1) {
		// 	currentview = new BetweenConditions(robot_idx, 0, robot_args, "collaborate");
		// } else {
		// 	currentview = new BetweenConditions(robot_idx, difficulty_idx + 1, robot_args, "observe");
		// }

		// if (difficulty_idx == difficulty_order.length - 1) {
		// 	if (robot_idx == robot_order.length - 1) {
		// 		currentview = new BetweenConditions(0, 0, robot_args, "collaborate");
		// 	} else {
		// 		currentview = new BetweenConditions(robot_idx + 1, 0, robot_args, "observe");
		// 	}
		// } else {
		// 	currentview = new BetweenConditions(robot_idx, difficulty_idx + 1, robot_args, "observe");
		// }
		// psiTurk.completeHIT();
	};
	color_arm_values(payoffs, probabilities);
	var ret = chooseNextArm();
	next_idx = ret[0];
	to_highlight = ret[1];
	highlight_arms(to_highlight);
	times_chosen[next_idx] += 1;
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
		num_arms = 10;
	} else {
		psiTurk.showPage('multiarm_bandit.html');
		num_arms = 4;
	}
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
	}

	var totalReward = 0;
	var prevReward = 0;
	var averages = new Array(num_arms).fill(0);
	var times_chosen = new Array(num_arms).fill(0);
	let [payoffs, probabilities] = initialize_arms(difficulty_order[difficulty_idx]);
	var iteration = 0;
	var next_idx;
	var to_highlight = _.range(num_arms);
	var next_disabled = false;
	var arms_disabled = false;
	var turn = "robot";
	var previous_arm_chosen;
	var pretrain_averages = [];

	//data to be recorded
	var all_times_chosen = [];
	var all_average_rewards = [];
	var all_total_rewards = [];
	var all_human_decisions = [];
	var all_robot_decisions = [];
	// var all_rewards = [];
	// var decisions = [];
	var all_pretrain_decisions = [];
	var all_pretrain_rewards = [];

	var chooseNextArm = function() {
		if (collaboration_type == "suggest" && iteration >= robot_args['pretrain']) {
			r = argmax(pretrain_averages);
			return [r, [r]];
		}

		if (robot_type == "random") {
			var r = Math.floor(Math.random()*num_arms);
			// first element for arm to pull
			// second array is for which arms to highlight, in case of multiple
			return [r, [r]];
		} else if (robot_type == "greedy" || robot_type == "greedy2") {
			var epsilon = robot_args['epsilon'];
			if (Math.random() > epsilon && iteration != 0) {
				// be greedy, pick argmax
				var r = argmax(averages);
				return [r, [r]];
			} else {
				// pick randomly
				var r = Math.floor(Math.random()*num_arms);
				return [r, _.range(num_arms)];
			}
		} else if (robot_type == "optimal") {
			if (iteration < num_arms) {
				// pick each arm once to begin
				return [iteration, [iteration]];
			}
			var avg_plus_conf = [];
			for (var i = 0; i < num_arms; i++) {
				avg_plus_conf.push(averages[i] + Math.sqrt(2 * Math.log(iteration) / times_chosen[i]))
			}
			var r = argmax(avg_plus_conf);
			return [r, [r]];
		}
	};

	var recordData = function(arm) {
		all_times_chosen.push(times_chosen.slice());
		all_average_rewards.push(averages.slice());
		all_total_rewards.push(totalReward);
		if (collaboration_type == "suggest") {
			all_robot_decisions.push(to_highlight);
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
	var recordPretrainData = function(arm) {
		all_pretrain_decisions.push(arm);
		all_pretrain_rewards.push(payoff);
	}

	clickArm = function(arm_idx, robot_click = false) {
		console.log(arms_disabled);
		if (arms_disabled && !robot_click) {
			return;
		}
		arms_disabled = true;
		unhighlight_arms(to_highlight);
		var r = Math.random();
		var payoff = 0;
		if (r < probabilities[arm_idx]) {
			payoff = payoffs[arm_idx];
		}

		// decisions.push(arm_idx);
		// all_rewards.push(payoff);

		averages[arm_idx] = ((averages[arm_idx] * times_chosen[arm_idx]) + payoff) / (times_chosen[arm_idx] + 1)
		times_chosen[arm_idx] += 1

		totalReward += payoff;
		prevReward = payoff;
		recordData(arm_idx);
		iteration += 1;
		previous_arm_chosen = arm_idx + 1;
		
		if (iteration >= NUM_ITERATIONS + robot_args["pretrain"]) {
			finish();
		}

		update();
		var ret = chooseNextArm();
		next_idx = ret[0];
		to_highlight = ret[1];
		highlight_arms(to_highlight);
		window.setTimeout(wait, 500);
	};

	var wait = function() {
		arms_disabled = false;
	}

	var pretrain = function(arm_idx) {
		if (arms_disabled) {
			return;
		}
		var r = Math.random();
		var payoff = 0;
		if (r < probabilities[arm_idx]) {
			payoff = payoffs[arm_idx];
		}

		averages[arm_idx] = ((averages[arm_idx] * times_chosen[arm_idx]) + payoff) / (times_chosen[arm_idx] + 1)
		times_chosen[arm_idx] += 1
		recordPretrainData(arm_idx);

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

	finish = function() {
		type = robot_type + "_" + difficulty + "_collaborate_" + collaboration_type
		all_data = {'robot_type': robot_type, 'difficulty': difficulty, 'robot_args': robot_args, 
					'collaboration_type': collaboration_type, 'total_reward': totalReward,
					'times_chosen': all_times_chosen, 'average_rewards': all_average_rewards, 
					'human_decisions': all_human_decisions, 'robot_decisions': all_robot_decisions,
					'all_rewards': all_total_rewards, 'arm_payoffs': payoffs, 'arm_probabilities': probabilities,
					'pretrain_decisions': all_pretrain_decisions, 'pretrain_rewards': all_pretrain_rewards};
		psiTurk.recordUnstructuredData(type, all_data);
		// psiTurk.recordUnstructuredData('robot_type', robot_type);
		// psiTurk.recordUnstructuredData('difficulty', difficulty);
		// psiTurk.recordUnstructuredData('robot_args', robot_args);
		// psiTurk.recordUnstructuredData('collaboration_type', collaboration_type);
		// psiTurk.recordUnstructuredData('total_reward_collab', totalReward);
		// psiTurk.recordUnstructuredData('decisions_collab', decisions);
		// psiTurk.recordUnstructuredData('times_chosen', all_times_chosen);
		// psiTurk.recordUnstructuredData('average_rewards', all_average_rewards);
		// psiTurk.recordUnstructuredData('human_decisions', human_decisions);
		// psiTurk.recordUnstructuredData('robot_decisions', robot_decisions);
		psiTurk.saveData();

		// unhighlight_arms([_.range(num_arms)]);
		arms_disabled = true;
		document.getElementById('finish').classList.remove("disabled");
		for (var i = 0; i < num_arms; i++) {
			document.getElementById('arm-' + String(i)).classList.add("disabled");
		}
		document.getElementById('finish').onclick = function() {
			if (difficulty_idx == difficulty_order.length - 1) {
				if (robot_idx == robot_order.length - 1) {
					currentview = new Questionnaire();
				} else {
					currentview = new BetweenConditions(robot_idx + 1, 0, robot_args, "observe");
				}
			} else {
				currentview = new BetweenConditions(robot_idx, difficulty_idx + 1, robot_args, "collaborate");
			}
		};

		// if (difficulty_idx == difficulty_order.length - 1) {
		// 	if (robot_idx == robot_order.length - 1) {
		// 		// psiTurk.completeHIT();
		// 		currentview = new Questionnaire();
		// 	} else {
		// 		currentview = new BetweenConditions(robot_idx + 1, 0, robot_args, "observe");
		// 	}
		// } else {
		// 	currentview = new BetweenConditions(robot_idx, difficulty_idx + 1, robot_args, "collaborate");
		// }

		// if (difficulty_idx == difficulty_order.length - 1) {
		// 	if (robot_idx == robot_order.length - 1) {
		// 		psiTurk.completeHIT();
		// 	} else {
		// 		currentview = new BetweenConditionsCollab(robot_idx + 1, 0, collaboration_idx, robot_args);
		// 	}
		// } else {
		// 	currentview = new BetweenConditionsCollab(robot_idx, difficulty_idx + 1, collaboration_idx, robot_args);
		// }
	};

	// Pretrain robot
	for (var i = 0; i < robot_args["pretrain"]; i++) {
		to_highlight = [];
		var ret = chooseNextArm();
		pretrain(ret[0]);
		all_pretrain_decisions.push()
	}
	pretrain_averages = averages.slice();
	// reset variables, iteration number necessary for math to work
	totalReward = 0;
	prevReward = 0;

	unhighlight_arms(_.range(num_arms));
	update();

	if (collaboration_type == "suggest") {
		var ret = chooseNextArm();
		next_idx = ret[0];
		to_highlight = ret[1];
		highlight_arms(to_highlight);
	}
};

var Questionnaire = function() {
	psiTurk.showPage('postquestionnaire.html');

	finish = function() {
		trust1 = document.querySelector('input[name="robot-green-trust"]:checked').value;
		trust2 = document.querySelector('input[name="robot-red-trust"]:checked').value;
		trust3 = document.querySelector('input[name="robot-yellow-trust"]:checked').value;
		psiTurk.recordUnstructuredData("trust_robot_green", trust1);
		psiTurk.recordUnstructuredData("trust_robot_red", trust2);
		psiTurk.recordUnstructuredData("trust_robot_yellow", trust3);
		psiTurk.saveData();
		psiTurk.completeHIT();
	}
}

// Task object to keep track of the current phase
var currentview;

/*******************
 * Run Task
 ******************/
$(window).load( function(){
    psiTurk.doInstructions(
    	instructionPages, // a list of pages you want to display in sequence
    	function() { // currentview = new ObserveRobot(0, 0, {"pretrain": 30, "epsilon": 0.1, "difficulty": "easy"}); 
    	// currentview = new Collaborate("optimal", {'pretrain': 0, "epsilon": 0.1, "difficulty": "hard"}, "turns");
    	// currentview = new BetweenConditions(0, 0, {"pretrain": 100, "epsilon": 0.1}, "observe");
    	// currentview = new Questionnaire();
    	currentview = new Training();
    }
    );
});
