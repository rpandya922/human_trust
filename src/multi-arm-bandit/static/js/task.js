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
	"observe_learning.html"
];

psiTurk.preloadPages(pages);

var instructionPages = [ // add as a list as many pages as you like
	"instructions/instruct-1.html",
];


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

	const num_arms = 4;
	var totalReward = 0;
	var prevReward = 0;
	var averages = [0, 0, 0, 0];
	var payoffs = [1, 2, 3, 4];
	var probabilities = [1, 1, 1, 1];
	var iteration = 0;
	var next_idx;

	var all_rewards = [];
	var decisions = [];

	var chooseNextArm = function() {
		if (robot_type == "random") {
			return Math.floor(Math.random()*num_arms);
		} else if (robot_type == "greedy") {
			var epsilon = robot_args['epsilon']
			if (Math.random() <= epsilon) {
				// be greedy, pick argmax
				return argmax(averages);
			} else {
				// pick randomly
				return Math.floor(Math.random()*num_arms);
			}
		} else if (robot_type == "optimal") {
			return 2;
		}
	};

	next_idx = chooseNextArm();
	document.getElementById("arm-" + String(next_idx)).classList.remove("btn-primary");
	document.getElementById("arm-" + String(next_idx)).classList.add("btn-success");

	next_iteration = function() {
		document.getElementById("arm-" + String(next_idx)).classList.add("active");
		window.setTimeout(finish_iteration, 1000);
	};
	var finish_iteration = function() {
		document.getElementById("arm-" + String(next_idx)).classList.remove("active");
		document.getElementById("arm-" + String(next_idx)).classList.remove("btn-success");
		document.getElementById("arm-" + String(next_idx)).classList.add("btn-primary");

		update();

		next_idx = chooseNextArm();
		document.getElementById("arm-" + String(next_idx)).classList.remove("btn-primary");
		document.getElementById("arm-" + String(next_idx)).classList.add("btn-success");
	};

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

	var update = function() {
		var r = Math.random();
		var payoff = 0;
		if (r < probabilities[next_idx]) {
			payoff = payoffs[next_idx];
		}

		decisions.push(next_idx);
		all_rewards.push(payoff);

		averages[next_idx] = ((averages[next_idx] * iteration) + payoff) / (iteration + 1)

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

	updateDisplay();
};

// Task object to keep track of the current phase
var currentview;

/*******************
 * Run Task
 ******************/
$(window).load( function(){
    psiTurk.doInstructions(
    	instructionPages, // a list of pages you want to display in sequence
    	function() { currentview = new ObserveRobot("greedy", {"epsilon": 0.1}); } // what you want to do when you are done with instructions
    );
});
