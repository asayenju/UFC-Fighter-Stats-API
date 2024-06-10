import requests
from bs4 import BeautifulSoup



def scrape_fighter_data(fighter_url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(fighter_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Helper function to safely extract text from a tag
    def extract_text(tag):
        return tag.text.strip() if tag else None

    def convert_to_float(percent_string):
        try:
            clean_string = percent_string.strip().replace('%', '')
            return float(clean_string)
        except (ValueError, AttributeError):
            return None

    # Extract fighter information
    name = extract_text(soup.find('h1', class_='hero-profile__name'))
    division_title = extract_text(soup.find('p', class_='hero-profile__division-title'))
    division_body = extract_text(soup.find('h1', class_='hero-profile__division-body'))

    try:
        division_body = soup.find('p', class_='hero-profile__division-body')
        division_text = division_body.text
        win, loss, draw = map(int, division_text.split(' ')[0].split('-'))
    except:
        win, loss, draw = None, None, None

    stats = {
        'name': name,
        'division_title': division_title,
        'win': win,
        'loss': loss,
        'draw': draw,
        'trains_at': None,
        'place_of_birth': None,
        'status': None,
        'fight_style': None,
        'age': None,
        'height': None,
        'weight': None,
        'ufc_debut': None,
        'reach': None,
        'leg_reach': None,
        'wins_by_knockout': None,
        'first_round_finishes': None,
        'striking_accuracy_percent': None,
        'significant_strikes_landed': None,
        'significant_strikes_attempted': None,
        'takedown_accuracy_percent': None,
        'takedowns_landed': None,
        'takedowns_attempted': None,
        'sig_str_landed_per_min': None,
        'sig_str_absorbed_per_min': None,
        'takedown_avg_per_15_min': None,
        'submission_avg_per_15_min': None,
        'sig_str_defense_percent': None,
        'takedown_defense_percent': None,
        'knockdown_avg': None,
        'average_fight_time': None,
        'sig_str_standing_amount': None,
        'sig_str_clinch_amount': None,
        'sig_str_ground_amount': None,
        'win_by_ko_tko_amount': None,
        'win_by_dec_amount': None,
        'win_by_sub_amount': None,
        'sig_str_standing_percentage': None,
        'sig_str_clinch_percentage': None,
        'sig_str_ground_percentage': None,
        'win_by_ko_tko_percentage': None,
        'win_by_dec_percentage': None,
        'win_by_sub_percentage': None,
        'strike_to_head': None,
        'strike_to_head_per': None,
        'strike_to_body': None,
        'strike_to_body_per': None,
        'strike_to_leg': None,
        'strike_to_leg_per': None
    }

    try:
        stat_divs = soup.find_all('div', class_='hero-profile__stat')
        for stat_div in stat_divs:
            stat_value = int(extract_text(stat_div.find('p', class_='hero-profile__stat-numb')))
            stat_description = extract_text(stat_div.find('p', class_='hero-profile__stat-text'))

            if stat_description == 'Wins by Knockout':
                stats['wins_by_knockout'] = stat_value
            elif stat_description == 'First Round Finishes':
                stats['first_round_finishes'] = stat_value
    except:
        pass

    try:
        # Find all <text> elements with class 'e-chart-circle__percent'
        percent_elements = soup.find_all('text', class_='e-chart-circle__percent')

        # Initialize variables to store accuracy percentages
        striking_accuracy_percentage = None
        takedown_accuracy_percentage = None

        # Iterate through the <text> elements
        for element in percent_elements:
            # Extract the accuracy percentage value
            accuracy_percentage = element.get_text().strip()

            # Check if it represents striking accuracy or takedown accuracy
            if 'Striking accuracy' in element.parent.find('title').get_text():
                striking_accuracy_percentage = convert_to_float(accuracy_percentage)
            elif 'Takedown Accuracy' in element.parent.find('title').get_text():
                takedown_accuracy_percentage = convert_to_float(accuracy_percentage)

        # Store accuracy percentages in the stats dictionary
        stats['striking_accuracy_percent'] = striking_accuracy_percentage
        stats['takedown_accuracy_percent'] = takedown_accuracy_percentage

    except Exception as e:
        #print("An error occurred while parsing accuracy percentages:", e)
        pass

    try:
        # Find the div for striking accuracy
        striking_accuracy_h2_tag = soup.find('h2', class_='e-t3', string='Striking accuracy')

        # Navigate to its parent div tag
        if striking_accuracy_h2_tag:
            striking_accuracy_title_tag = striking_accuracy_h2_tag.parent
        else:
            raise ValueError("Striking Accuracy title tag not found.")

        # Find significant strikes landed and attempted
        striking_dl = striking_accuracy_title_tag.find_next_sibling('div', class_='c-overlap__stats-wrap')
        if striking_dl:
            sig_strikes_landed_tag = striking_dl.find('dt', class_='c-overlap__stats-text', string='Sig. Strikes Landed')
            if sig_strikes_landed_tag:
                sig_strikes_landed = sig_strikes_landed_tag.find_next_sibling('dd', class_='c-overlap__stats-value').text.strip()
                # Check if sig_strikes_landed is blank, if so, set it to None
                sig_strikes_landed = None if not sig_strikes_landed else int(sig_strikes_landed)
                stats['significant_strikes_landed'] = sig_strikes_landed

            # Find significant strikes attempted
            sig_strikes_attempted_tag = striking_dl.find('dt', class_='c-overlap__stats-text', string='Sig. Strikes Attempted')
            if sig_strikes_attempted_tag:
                sig_strikes_attempted = sig_strikes_attempted_tag.find_next_sibling('dd', class_='c-overlap__stats-value').text.strip()
                # Check if sig_strikes_attempted is blank, if so, set it to None
                sig_strikes_attempted = None if not sig_strikes_attempted else int(sig_strikes_attempted)
                stats['significant_strikes_attempted'] = sig_strikes_attempted

    except Exception as e:
        #print("An error occurred while parsing striking accuracy stats:", e)
        pass

    try:
        # Find the div for takedown accuracy
        takedown_accuracy_h2_tag = soup.find('h2', class_='e-t3', string='Takedown Accuracy')

        # Navigate to its parent div tag
        if takedown_accuracy_h2_tag:
            takedown_accuracy_title_tag = takedown_accuracy_h2_tag.parent
        else:
            raise ValueError("Takedown Accuracy title tag not found.")

        # Find takedowns landed and attempted
        takedown_dl = takedown_accuracy_title_tag.find_next_sibling('div', class_='c-overlap__stats-wrap')
        if takedown_dl:
            takedowns_landed_tag = takedown_dl.find('dt', class_='c-overlap__stats-text', string='Takedowns Landed')
            if takedowns_landed_tag:
                takedowns_landed = takedowns_landed_tag.find_next_sibling('dd', class_='c-overlap__stats-value').text.strip()
                # Check if takedowns_landed is blank, if so, set it to None
                takedowns_landed = None if not takedowns_landed else int(takedowns_landed)
                stats['takedowns_landed'] = takedowns_landed

            # Find takedowns attempted
            takedowns_attempted_tag = takedown_dl.find('dt', class_='c-overlap__stats-text', string='Takedowns Attempted')
            if takedowns_attempted_tag:
                takedowns_attempted = takedowns_attempted_tag.find_next_sibling('dd', class_='c-overlap__stats-value').text.strip()
                # Check if takedowns_attempted is blank, if so, set it to None
                takedowns_attempted = None if not takedowns_attempted else int(takedowns_attempted)
                stats['takedowns_attempted'] = takedowns_attempted

    except Exception as e:
        #print("An error occurred while parsing takedown accuracy stats:", e)
        pass

    if stats['striking_accuracy_percent'] is None and stats['significant_strikes_landed'] is not None and stats['significant_strikes_attempted'] is not None:
        stats['striking_accuracy_percent'] = (stats['significant_strikes_landed'] / stats['significant_strikes_attempted']) * 100

    if stats['takedown_accuracy_percent'] is None and stats['takedowns_landed'] is not None and stats['takedowns_attempted'] is not None:
        stats['takedown_accuracy_percent'] = (stats['takedowns_landed'] / stats['takedowns_attempted']) * 100


    try:
        # Find all div elements with class 'c-stat-compare__group-1'
        stats_group_1_elements = soup.find_all('div', class_='c-stat-compare__group-1')

        # Initialize variables to store stats
        sig_str_landed_per_min = None
        takedown_avg_per_15_min = None
        sig_str_defense_percent = None
        knockdown_avg = None
        

        # Iterate through the elements
        for element in stats_group_1_elements:
            # Extract the stat number and label
            stat_number = element.find(class_='c-stat-compare__number').get_text().strip()
            stat_label = element.find(class_='c-stat-compare__label').get_text().strip()

            # Check the label and assign the value accordingly
            if 'Sig. Str. Landed' in stat_label:
                sig_str_landed_per_min = float(stat_number)
            elif 'Takedown avg' in stat_label:
                takedown_avg_per_15_min = float(stat_number)
            elif 'Sig. Str. Defense' in stat_label:
                sig_str_defense_percent = convert_to_float(stat_number)
            elif 'Knockdown Avg' in stat_label:
                knockdown_avg = float(stat_number)

        stats['sig_str_landed_per_min'] = sig_str_landed_per_min
        stats['takedown_avg_per_15_min'] = takedown_avg_per_15_min
        stats['sig_str_defense_percent'] = sig_str_defense_percent
        stats['knockdown_avg'] = knockdown_avg

    except Exception as e:
        #print("An error occurred while parsing stats group 1:", e)
        pass

    try:
        # Find all div elements with class 'c-stat-compare__group-1'
        stats_group_2_elements = soup.find_all('div', class_='c-stat-compare__group-2')

        # Initialize variables to store stats
        sig_str_absorbed_per_min = None
        submission_avg_per_15_min = None
        takedown_defense_percent = None
        average_fight_time = None
        

        # Iterate through the elements
        for element in stats_group_2_elements:
            # Extract the stat number and label
            stat_number = element.find(class_='c-stat-compare__number').get_text().strip()
            stat_label = element.find(class_='c-stat-compare__label').get_text().strip()

            # Check the label and assign the value accordingly
            if 'Sig. Str. Absorbed' in stat_label:
                sig_str_absorbed_per_min = float(stat_number)
            elif 'Submission avg' in stat_label:
                submission_avg_per_15_min = float(stat_number)
            elif 'Takedown Defense' in stat_label:
                takedown_defense_percent = convert_to_float(stat_number)
            elif 'Average fight time' in stat_label:
                average_fight_time = stat_number

        stats['sig_str_absorbed_per_min'] = sig_str_absorbed_per_min
        stats['submission_avg_per_15_min'] = submission_avg_per_15_min
        stats['takedown_defense_percent'] = takedown_defense_percent
        stats['average_fight_time'] = average_fight_time

    except Exception as e:
        #print("An error occurred while parsing stats group 1:", e)
        pass

    try:
        # Store all values and percentages in an array
        value_percent_pairs = []

        # Find all value/percentage pairs in Sig. Str. By Position section
        sig_str_position_div = soup.find('h2', class_='c-stat-3bar__title', string='Sig. Str. By Position')
        if sig_str_position_div:
            position_groups = sig_str_position_div.find_next('div', class_='c-stat-3bar__legend').find_all('div', class_='c-stat-3bar__group')
            for group in position_groups:
                label = group.find('div', class_='c-stat-3bar__label').get_text(strip=True)
                value = group.find('div', class_='c-stat-3bar__value').get_text(strip=True)
                value_percent_pairs.append((label, value))

        # Find all value/percentage pairs in Win by Method section
        win_by_method_div = soup.find('h2', class_='c-stat-3bar__title', string='Win by Method')
        if win_by_method_div:
            method_groups = win_by_method_div.find_next('div', class_='c-stat-3bar__legend').find_all('div', class_='c-stat-3bar__group')
            for group in method_groups:
                label = group.find('div', class_='c-stat-3bar__label').get_text(strip=True)
                value = group.find('div', class_='c-stat-3bar__value').get_text(strip=True)
                value_percent_pairs.append((label, value))

        # Process the value/percentage pairs and assign them to the correct variables
        for label, value in value_percent_pairs:
            if ' ' in value:
                amount, percentage = value.split(' ')
                amount = int(amount)
                percentage = float(percentage.strip('()%'))
            else:
                amount = int(value)
                percentage = None

            if label.lower() == 'standing':
                stats['sig_str_standing_amount'] = amount
                stats['sig_str_standing_percentage'] = percentage
            elif label.lower() == 'clinch':
                stats['sig_str_clinch_amount'] = amount
                stats['sig_str_clinch_percentage'] = percentage
            elif label.lower() == 'ground':
                stats['sig_str_ground_amount'] = amount
                stats['sig_str_ground_percentage'] = percentage
            elif label.lower() == 'ko/tko':
                stats['win_by_ko_tko_amount'] = amount
                stats['win_by_ko_tko_percentage'] = percentage
            elif label.lower() == 'dec':
                stats['win_by_dec_amount'] = amount
                stats['win_by_dec_percentage'] = percentage
            elif label.lower() == 'sub':
                stats['win_by_sub_amount'] = amount
                stats['win_by_sub_percentage'] = percentage

    except Exception as e:
        #print(f"An error occurred while parsing stats: {e}")
        pass

    try:
        stats['strike_to_head'] = int(soup.find('text', id='e-stat-body_x5F__x5F_head_value').text)
        stats['strike_to_head_per'] = float(soup.find('text', id='e-stat-body_x5F__x5F_head_percent').text.strip('%'))
        stats['strike_to_body'] = int(soup.find('text', id='e-stat-body_x5F__x5F_body_value').text)
        stats['strike_to_body_per'] = float(soup.find('text', id='e-stat-body_x5F__x5F_body_percent').text.strip('%'))
        stats['strike_to_leg'] = int(soup.find('text', id='e-stat-body_x5F__x5F_leg_value').text)
        stats['strike_to_leg_per'] = float(soup.find('text', id='e-stat-body_x5F__x5F_leg_percent').text.strip('%'))
    except:
        pass

    try:

        fields = soup.find_all(class_='c-bio__field')
# Iterate over rows
        for field in fields:
            label_element = field.find(class_='c-bio__label')
            if label_element:
                label = label_element.text.strip()
                text_element = field.find(class_='c-bio__text')
                if text_element:
                    text = text_element.get_text(strip=True)

                    if label.lower() == "status":
                        stats['status'] = text
                    elif label.lower() == "place of birth":
                        stats['place_of_birth'] = text
                    elif label.lower() == "trains at":
                        stats['trains_at'] = text
                    elif label.lower() == "fighting style":
                        stats['fight_style'] = text
                    elif label.lower() == "age":
                        stats['age'] = int(text)
                    elif label.lower() == "height":
                        stats['height'] = float(text)
                    elif label.lower() == "weight":
                        stats['weight'] = float(text)
                    elif label.lower() == "octagon debut":
                        stats['ufc_debut'] = text
                    elif label.lower() == "reach":
                        stats['reach'] = float(text)
                    elif label.lower() == "leg reach":
                        stats['leg_reach'] = float(text)

    except Exception as e:
        #print(f"An error occurred while parsing fighter bio: {e}")
        pass

    return stats