window.onload = function() {

	//Получение из DOM массивов с ссылками и selectами
	let categorySelect = document.querySelectorAll("#category_select")[0];
	let locationSelect = document.querySelectorAll("#location_select")[0];
	let links = Array.from(document.querySelectorAll(".news_links a"));
	let politics = Array.from(document.querySelectorAll(".politics"));
	let economy = Array.from(document.querySelectorAll(".economy"));
	let accidents = Array.from(document.querySelectorAll(".accidents"));
	let society = Array.from(document.querySelectorAll(".society"));
	let culture = Array.from(document.querySelectorAll(".culture"));
	let sport = Array.from(document.querySelectorAll(".sport"));
	let region = Array.from(document.querySelectorAll(".region"));
	let siberia = Array.from(document.querySelectorAll(".siberia"));
	let russia = Array.from(document.querySelectorAll(".russia"));
	let world = Array.from(document.querySelectorAll(".world"));

	//Функция для изменения видимости элементов(ссылок)
	function displayToggle(show, ...args) {
		show.forEach(item => item.style.display = "block");
		
		for (i = 0; i < args.length; i++) {
			args[i].forEach(item => item.style.display = "none");
		}
	}

	//При изменении выбора в выпадающих списках, будет использоваться функция
	//для перебора условий и изменения видимости
	function conditionCheck() {
		if (categorySelect.value == "all_categories" && locationSelect.value == "all_regions") {
			displayToggle(links);
		} else if (categorySelect.value == "all_categories" && locationSelect.value == "region") {
			displayToggle(links, siberia, russia, world);
		} else if (categorySelect.value == "all_categories" && locationSelect.value == "siberia") {
			displayToggle(links, region, russia, world);
		} else if (categorySelect.value == "all_categories" && locationSelect.value == "russia") {
			displayToggle(links, region, siberia, world);
		} else if (categorySelect.value == "all_categories" && locationSelect.value == "world") {
			displayToggle(links, region, siberia, russia);
		} else if (categorySelect.value == "politics" && locationSelect.value == "all_regions") {
			displayToggle(links, economy, accidents, society, culture, sport);
		} else if (categorySelect.value == "politics" && locationSelect.value == "region") {
			displayToggle(links, siberia, russia, world, economy, accidents, society, culture, sport);
		} else if (categorySelect.value == "politics" && locationSelect.value == "siberia") {
			displayToggle(links, region, russia, world, economy, accidents, society, culture, sport);
		} else if (categorySelect.value == "politics" && locationSelect.value == "russia") {
			displayToggle(links, region, siberia, world, economy, accidents, society, culture, sport);
		} else if (categorySelect.value == "politics" && locationSelect.value == "world") {
			displayToggle(links, region, siberia, russia, economy, accidents, society, culture, sport);
		} else if (categorySelect.value == "economy" && locationSelect.value == "all_regions") {
			displayToggle(links, politics, accidents, society, culture, sport);
		} else if (categorySelect.value == "economy" && locationSelect.value == "region") {
			displayToggle(links, siberia, russia, world, politics, accidents, society, culture, sport);
		} else if (categorySelect.value == "economy" && locationSelect.value == "siberia") {
			displayToggle(links, region, russia, world, politics, accidents, society, culture, sport);
		} else if (categorySelect.value == "economy" && locationSelect.value == "russia") {
			displayToggle(links, region, siberia, world, politics, accidents, society, culture, sport);
		} else if (categorySelect.value == "economy" && locationSelect.value == "world") {
			displayToggle(links, region, siberia, russia, politics, accidents, society, culture, sport);
		} else if (categorySelect.value == "accidents" && locationSelect.value == "all_regions") {
			displayToggle(links, politics, economy, society, culture, sport);
		} else if (categorySelect.value == "accidents" && locationSelect.value == "region") {
			displayToggle(links, siberia, russia, world, politics, economy, society, culture, sport);
		} else if (categorySelect.value == "accidents" && locationSelect.value == "siberia") {
			displayToggle(links, region, russia, world, politics, economy, society, culture, sport);
		} else if (categorySelect.value == "accidents" && locationSelect.value == "russia") {
			displayToggle(links, region, siberia, world, politics, economy, society, culture, sport);
		} else if (categorySelect.value == "accidents" && locationSelect.value == "world") {
			displayToggle(links, region, siberia, russia, politics, economy, society, culture, sport);
		} else if (categorySelect.value == "society" && locationSelect.value == "all_regions") {
			displayToggle(links, politics, economy, accidents, culture, sport);
		} else if (categorySelect.value == "society" && locationSelect.value == "region") {
			displayToggle(links, siberia, russia, world, politics, economy, accidents, culture, sport);
		} else if (categorySelect.value == "society" && locationSelect.value == "siberia") {
			displayToggle(links, region, russia, world, politics, economy, accidents, culture, sport);
		} else if (categorySelect.value == "society" && locationSelect.value == "russia") {
			displayToggle(links, region, siberia, world, politics, economy, accidents, culture, sport);
		} else if (categorySelect.value == "society" && locationSelect.value == "world") {
			displayToggle(links, region, siberia, russia, politics, economy, accidents, culture, sport);
		} else if (categorySelect.value == "culture" && locationSelect.value == "all_regions") {
			displayToggle(links, politics, economy, accidents, society, sport);
		} else if (categorySelect.value == "culture" && locationSelect.value == "region") {
			displayToggle(links, siberia, russia, world, politics, economy, accidents, society, sport);
		} else if (categorySelect.value == "culture" && locationSelect.value == "siberia") {
			displayToggle(links, region, russia, world, politics, economy, accidents, society, sport);
		} else if (categorySelect.value == "culture" && locationSelect.value == "russia") {
			displayToggle(links, region, siberia, world, politics, economy, accidents, society, sport);
		} else if (categorySelect.value == "culture" && locationSelect.value == "world") {
			displayToggle(links, region, siberia, russia, politics, economy, accidents, society, sport);
		} else if (categorySelect.value == "sport" && locationSelect.value == "all_regions") {
			displayToggle(links, politics, economy, accidents, society, culture);
		} else if (categorySelect.value == "sport" && locationSelect.value == "region") {
			displayToggle(links, siberia, russia, world, politics, economy, accidents, society, culture);
		} else if (categorySelect.value == "sport" && locationSelect.value == "siberia") {
			displayToggle(links, region, russia, world, politics, economy, accidents, society, culture);
		} else if (categorySelect.value == "sport" && locationSelect.value == "russia") {
			displayToggle(links, region, siberia, world, politics, economy, accidents, society, culture);
		} else if (categorySelect.value == "sport" && locationSelect.value == "world") {
			displayToggle(links, region, siberia, russia, politics, economy, accidents, society, culture);
		}
	}

	categorySelect.onchange = conditionCheck;
	locationSelect.onchange = conditionCheck;
}