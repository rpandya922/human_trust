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
	"observe_learning.html"
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
var OPTIMAL_COLOR = 'btn-primary';
var RANDOM_COLOR = 'btn-warning';

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
		document.getElementById("arm-" + String(arms[i])).classList.remove(HIGHLIGHT_COLOR);
		document.getElementById("arm-" + String(arms[i])).classList.add(DEFAULT_COLOR);
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

var TrustExperiment = function() {
	psiTurk.showPage('multiarm_bandit.html');

	var totalReward = 0;
	var prevReward = 0;
	var averages = [0, 0, 0, 0];
	var payoffs = [1, 2, 3, 4];
	var probabilities = [1, 1, 1, 1];
	var iteration = 0;

	var all_rewards = [];
	var decisions = [];

	clickArm = function(arm_idx) {
		var r = Math.random();
		var payoff = 0;
		if (r < probabilities[arm_idx]) {
			payoff = payoffs[arm_idx];
		}

		decisions.push(arm_idx);
		all_rewards.push(payoff);

		totalReward += payoff;
		prevReward = payoff;
		iteration += 1;
		if (iteration >= 30) {
			finish();
		}
		update();
	};
	var update = function() {
		d3.select("#reward").text(totalReward);
		d3.select("#previous-reward").text(prevReward);
		d3.select("#iteration").text(iteration);
	};
	finish = function() {
		psiTurk.recordUnstructuredData('total_reward', totalReward);
		psiTurk.recordUnstructuredData('decisions', decisions);
		psiTurk.saveData();
		psiTurk.completeHIT();
	};

	// $("#arm-1").click(function() {
	// 	clickArm(1);
	// });

	update();
};

var ObserveRobot = function(robot_type, robot_args) {
	psiTurk.showPage('observe_learning.html');

	if (robot_type == "random") {
		HIGHLIGHT_COLOR = RANDOM_COLOR;
	} else if (robot_type == "optimal") {
		HIGHLIGHT_COLOR = OPTIMAL_COLOR;
	} else if (robot_type == "greedy") {
		HIGHLIGHT_COLOR = GREEDY_COLOR;
	}

	const num_arms = 4;
	var totalReward = 0;
	var prevReward = 0;
	var averages = [0, 0, 0, 0];
	var times_chosen = [0, 0, 0, 0];
	var payoffs = [1, 2, 3, 4];
	var probabilities = [1, 1, 1, 1];
	var iteration = 0;
	var next_idx;
	var to_highlight;
	var click_disabled = false;

	var all_rewards = [];
	var decisions = [];

	var chooseNextArm = function() {
		if (robot_type == "random") {
			var r = Math.floor(Math.random()*num_arms);
			// first element for arm to pull
			// second array is for which arms to highlight, in case of multiple
			return [r, [r]];
		} else if (robot_type == "greedy") {
			var epsilon = robot_args['epsilon'];
			if (Math.random() > epsilon) {
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

	next_iteration = function() {
		if (click_disabled) {
			return;
		}
		document.getElementById("arm-" + String(next_idx)).classList.add("active");
		click_disabled = true;
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

		decisions.push(next_idx);
		all_rewards.push(payoff);

		averages[next_idx] = ((averages[next_idx] * times_chosen[next_idx]) + payoff) / (times_chosen[next_idx] + 1)

		totalReward += payoff;
		prevReward = payoff;
		iteration += 1;
		if (iteration >= 30) {
			finish();
		}
		updateDisplay();
	};

	var updateDisplay = function() {
		d3.select("#reward").text(totalReward);
		d3.select("#previous-reward").text(prevReward);
		d3.select("#iteration").text(iteration);
	};

	finish = function() {
		psiTurk.recordUnstructuredData('total_reward', totalReward);
		psiTurk.recordUnstructuredData('decisions', decisions);
		psiTurk.saveData();
		psiTurk.completeHIT();
	};

	var ret = chooseNextArm();
	next_idx = ret[0];
	to_highlight = ret[1];
	highlight_arms(to_highlight);
	times_chosen[next_idx] += 1;
	updateDisplay();
};

var Collaborate = function(robot_type, robot_args, collaboration_type) {
	var num_arms;
	if (robot_args["difficulty"] == "easy") {
		psiTurk.showPage('multiarm_bandit_easy.html');
		num_arms = 2;
	} else if (robot_args["difficulty"] == "hard") {
		psiTurk.showPage('multiarm_bandit_hard.html');
		num_arms = 10;
	} else {
		psiTurk.showPage('multiarm_bandit.html');
		num_arms = 4;
	}

	if (robot_type == "random") {
		HIGHLIGHT_COLOR = RANDOM_COLOR;
	} else if (robot_type == "optimal") {
		HIGHLIGHT_COLOR = OPTIMAL_COLOR;
	} else if (robot_type == "greedy") {
		HIGHLIGHT_COLOR = GREEDY_COLOR;
		try {
			var e = robot_args['epsilon'];
		} catch(err) {
			throw "Need epsilon parameter for greedy robot";
		}
	}

	var totalReward = 0;
	var prevReward = 0;
	var averages = new Array(num_arms).fill(0);
	var times_chosen = new Array(num_arms).fill(0);
	var payoffs = _.range(num_arms);
	var probabilities = new Array(num_arms).fill(1);
	var iteration = 0;
	var next_idx;
	var to_highlight = _.range(num_arms);
	var next_disabled = false;
	var arms_disabled = false;
	var turn = "robot";

	var all_rewards = [];
	var decisions = [];

	var chooseNextArm = function() {
		if (robot_type == "random") {
			var r = Math.floor(Math.random()*num_arms);
			// first element for arm to pull
			// second array is for which arms to highlight, in case of multiple
			return [r, [r]];
		} else if (robot_type == "greedy") {
			var epsilon = robot_args['epsilon'];
			if (Math.random() > epsilon) {
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

	clickArm = function(arm_idx, robot_click = false) {
		if (arms_disabled && !robot_click) {
			return;
		}
		unhighlight_arms(to_highlight);
		var r = Math.random();
		var payoff = 0;
		if (r < probabilities[arm_idx]) {
			payoff = payoffs[arm_idx];
		}

		decisions.push(arm_idx);
		all_rewards.push(payoff);

		averages[arm_idx] = ((averages[arm_idx] * times_chosen[arm_idx]) + payoff) / (times_chosen[arm_idx] + 1)
		times_chosen[arm_idx] += 1

		totalReward += payoff;
		prevReward = payoff;
		iteration += 1;
		
		if (iteration >= 30 + robot_args["pretrain"]) {
			finish();
		}

		update();
		var ret = chooseNextArm();
		next_idx = ret[0];
		to_highlight = ret[1];
		highlight_arms(to_highlight);
	};

	var pretrain = function(arm_idx) {
		if (arms_disabled) {
			return;
		}
		var r = Math.random();
		var payoff = 0;
		if (r < probabilities[arm_idx]) {
			payoff = payoffs[arm_idx];
		}

		decisions.push(arm_idx);
		all_rewards.push(payoff);

		averages[arm_idx] = ((averages[arm_idx] * times_chosen[arm_idx]) + payoff) / (times_chosen[arm_idx] + 1)
		times_chosen[arm_idx] += 1

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
		console.log(times_chosen);
		console.log(averages);
	};

	finish = function() {
		psiTurk.recordUnstructuredData('total_reward', totalReward);
		psiTurk.recordUnstructuredData('decisions', decisions);
		psiTurk.saveData();
		psiTurk.completeHIT();
	};

	// Pretrain robot
	for (var i = 0; i < robot_args["pretrain"]; i++) {
		to_highlight = [];
		var ret = chooseNextArm();
		pretrain(ret[0]);
	}
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

// Task object to keep track of the current phase
var currentview;

/*******************
 * Run Task
 ******************/
$(window).load( function(){
    psiTurk.doInstructions(
    	instructionPages, // a list of pages you want to display in sequence
    	function() { //currentview = new ObserveRobot("optimal", {"epsilon": 0.1}); 
    	currentview = new Collaborate("optimal", {'pretrain': 0, "epsilon": 0.1, "difficulty": "hard"}, "turns");
    }
    );
});
