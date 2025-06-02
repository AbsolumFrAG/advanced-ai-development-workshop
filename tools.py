"""
LXP - Advanced AI development Workshop: FBI API Chatbot tools

WARNING: LangChain ConversationalAgent only accepts single input parameters for tool calling.
Use create_string_input_tool() to wrap multi-parameter functions.
"""

import requests
from langchain_core.tools import tool
from utils import create_string_input_tool

@tool
def get_fbi_most_wanted() -> str:
    """Get the list of FBI's most wanted persons with comprehensive details.
    
    Returns:
        A formatted string with detailed information about the most wanted persons
    """
    try:
        # Get the most wanted list from FBI API
        url = "https://api.fbi.gov/wanted/v1/list"
        params = {
            'pageSize': 10,  # Limit to 10 results for readability
            'page': 1,
            'sort_on': 'publication',
            'sort_order': 'desc'
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if not data.get('items'):
            return "No wanted persons found in the FBI database."
        
        result = "🚨 FBI MOST WANTED LIST 🚨\n\n"
        
        for i, person in enumerate(data['items'][:8], 1):  # Show top 8
            name = person.get('title', 'Unknown')
            subjects = person.get('subjects', ['Unknown'])
            reward = person.get('reward_text', 'No reward specified')
            status = person.get('status', 'na')
            field_offices = person.get('field_offices', [])
            publication = person.get('publication', 'Unknown date')[:10]  # Just date part
            
            # Status indicator
            status_icon = "🔴" if status == "na" else "🟢"
            status_text = "ACTIVE" if status == "na" else "CAPTURED"
            
            result += f"{i}. **{name}** {status_icon} {status_text}\n"
            result += f"   📂 Subjects: {', '.join(subjects)}\n"
            result += f"   💰 Reward: {reward}\n"
            result += f"   📅 Published: {publication}\n"
            
            if field_offices:
                result += f"   🏢 Field Office: {', '.join(field_offices).title()}\n"
            
            # Add warning if present
            if person.get('warning_message'):
                result += f"   ⚠️ WARNING: {person['warning_message']}\n"
            
            # Add description if available
            if person.get('description'):
                desc = person['description'][:150] + "..." if len(person['description']) > 150 else person['description']
                result += f"   📋 Description: {desc}\n"
            
            # Add caution if available
            if person.get('caution'):
                caution_text = person['caution']
                # Remove HTML tags for cleaner display
                import re
                caution_clean = re.sub('<[^<]+?>', '', caution_text)[:200] + "..."
                result += f"   ⚠️ Details: {caution_clean}\n"
            
            result += f"   🆔 ID: {person.get('uid', 'No ID')}\n\n"
        
        result += f"📊 Total persons in database: {data.get('total', 'Unknown')}\n"
        result += f"📄 Showing page {data.get('page', 1)} of results"
        
        return result
        
    except Exception as e:
        return f"Error retrieving FBI most wanted list: {str(e)}"

@tool  
def search_fbi_person_by_name(name: str) -> str:
    """Search for a specific person in the FBI wanted database by name with comprehensive details.
    
    Args:
        name: The name of the person to search for
        
    Returns:
        A formatted string with detailed information about the person if found
    """
    try:
        url = "https://api.fbi.gov/wanted/v1/list"
        params = {
            'title': name,
            'pageSize': 5
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if not data.get('items'):
            return f"No person named '{name}' found in the FBI wanted database."
        
        result = f"🔍 SEARCH RESULTS FOR '{name.upper()}'\n\n"
        
        for i, person in enumerate(data['items'], 1):
            title = person.get('title', 'Unknown')
            uid = person.get('uid', 'Unknown')
            subjects = person.get('subjects', ['Unknown'])
            reward = person.get('reward_text', 'No reward specified')
            publication_date = person.get('publication', 'Unknown date')[:10]
            status = person.get('status', 'na')
            field_offices = person.get('field_offices', [])
            
            # Personal details
            sex = person.get('sex', 'Unknown')
            race = person.get('race_raw', person.get('race', 'Unknown'))
            hair = person.get('hair_raw', person.get('hair', 'Unknown'))
            eyes = person.get('eyes_raw', person.get('eyes', 'Unknown'))
            height = f"{person.get('height_min', 0)//12}'{person.get('height_min', 0)%12}\"" if person.get('height_min') else 'Unknown'
            weight = person.get('weight', 'Unknown')
            
            # Birth info
            birth_dates = person.get('dates_of_birth_used', [])
            birth_place = person.get('place_of_birth', 'Unknown')
            nationality = person.get('nationality', 'Unknown')
            aliases = person.get('aliases', [])
            
            # Status indicator
            status_icon = "🔴" if status == "na" else "🟢"
            status_text = "ACTIVE" if status == "na" else "CAPTURED"
            
            result += f"**{i}. {title}** {status_icon} {status_text}\n"
            result += f"🆔 ID: {uid}\n"
            result += f"📂 Subjects: {', '.join(subjects)}\n"
            result += f"💰 Reward: {reward}\n"
            result += f"📅 Publication: {publication_date}\n"
            
            if field_offices:
                result += f"🏢 Field Office: {', '.join(field_offices).title()}\n"
            
            # Physical description
            result += f"\n👤 **PHYSICAL DESCRIPTION:**\n"
            result += f"   Sex: {sex} | Race: {race}\n"
            result += f"   Height: {height} | Weight: {weight}\n"
            result += f"   Hair: {hair} | Eyes: {eyes}\n"
            
            # Personal information
            if birth_dates or birth_place != 'Unknown' or nationality != 'Unknown':
                result += f"\n📋 **PERSONAL INFO:**\n"
                if birth_dates:
                    result += f"   Birth Date(s): {', '.join(birth_dates)}\n"
                if birth_place != 'Unknown':
                    result += f"   Birth Place: {birth_place}\n"
                if nationality != 'Unknown':
                    result += f"   Nationality: {nationality}\n"
            
            # Aliases
            if aliases:
                result += f"   Aliases: {', '.join(aliases)}\n"
            
            # Warning
            if person.get('warning_message'):
                result += f"\n⚠️ **WARNING:** {person['warning_message']}\n"
            
            # Description
            if person.get('description'):
                desc = person['description'][:300] + "..." if len(person['description']) > 300 else person['description']
                result += f"\n📄 **DESCRIPTION:** {desc}\n"
            
            # Caution details
            if person.get('caution'):
                import re
                caution_clean = re.sub('<[^<]+?>', '', person['caution'])[:400] + "..."
                result += f"\n🚨 **CAUTION:** {caution_clean}\n"
            
            # Additional details
            if person.get('details'):
                import re
                details_clean = re.sub('<[^<]+?>', '', person['details'])[:300] + "..."
                result += f"\n📝 **DETAILS:** {details_clean}\n"
            
            # Scars and marks
            if person.get('scars_and_marks'):
                result += f"\n🔍 **SCARS & MARKS:** {person['scars_and_marks']}\n"
            
            # Remarks
            if person.get('remarks'):
                import re
                remarks_clean = re.sub('<[^<]+?>', '', person['remarks'])[:200] + "..."
                result += f"\n💭 **REMARKS:** {remarks_clean}\n"
            
            result += "\n" + "="*60 + "\n"
        
        return result
        
    except Exception as e:
        return f"Error searching for person '{name}': {str(e)}"

def search_fbi_by_field_office(field_office: str, page_size: str = "10") -> str:
    """Search FBI wanted persons by field office.
    
    Args:
        field_office: FBI field office name (e.g., "newyork", "losangeles", "chicago")
        page_size: Number of results to return (default: 10, max: 50)
        
    Returns:
        A formatted string with search results from the specified field office
    """
    try:
        url = "https://api.fbi.gov/wanted/v1/list"
        params = {
            'field_offices': field_office.lower(),
            'pageSize': min(int(page_size), 50)  # API limit
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if not data.get('items'):
            return f"No wanted persons found for field office: {field_office}"
        
        result = f"🏢 FBI FIELD OFFICE: {field_office.upper()}\n\n"
        
        for i, person in enumerate(data['items'], 1):
            name = person.get('title', 'Unknown')
            subjects = person.get('subjects', ['Unknown'])
            reward = person.get('reward_text', 'No reward specified')
            
            result += f"{i}. **{name}**\n"
            result += f"   Subjects: {', '.join(subjects)}\n"
            result += f"   Reward: {reward}\n"
            
            if person.get('description'):
                desc = person['description'][:150] + "..." if len(person['description']) > 150 else person['description']
                result += f"   Description: {desc}\n"
            
            result += "\n"
        
        result += f"Total results: {data.get('total', 'Unknown')} from {field_office} field office"
        
        return result
        
    except Exception as e:
        return f"Error searching field office '{field_office}': {str(e)}"

def search_fbi_by_status(status: str, page_size: str = "10") -> str:
    """Search FBI wanted persons by status.
    
    Args:
        status: Status of the wanted person (e.g., "captured", "na" for not applicable)
        page_size: Number of results to return (default: 10, max: 50)
        
    Returns:
        A formatted string with search results matching the specified status
    """
    try:
        url = "https://api.fbi.gov/wanted/v1/list"
        params = {
            'status': status.lower(),
            'pageSize': min(int(page_size), 50)
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if not data.get('items'):
            return f"No wanted persons found with status: {status}"
        
        result = f"📊 STATUS SEARCH: {status.upper()}\n\n"
        
        for i, person in enumerate(data['items'], 1):
            name = person.get('title', 'Unknown')
            subjects = person.get('subjects', ['Unknown'])
            reward = person.get('reward_text', 'No reward specified')
            publication = person.get('publication', 'Unknown date')
            
            result += f"{i}. **{name}**\n"
            result += f"   Subjects: {', '.join(subjects)}\n"
            result += f"   Status: {status}\n"
            result += f"   Reward: {reward}\n"
            result += f"   Publication: {publication}\n"
            
            if person.get('description'):
                desc = person['description'][:120] + "..." if len(person['description']) > 120 else person['description']
                result += f"   Description: {desc}\n"
            
            result += "\n"
        
        result += f"Total results: {data.get('total', 'Unknown')} with status '{status}'"
        
        return result
        
    except Exception as e:
        return f"Error searching by status '{status}': {str(e)}"

def search_fbi_by_classification(classification: str, page_size: str = "10") -> str:
    """Search FBI wanted persons by person classification.
    
    Args:
        classification: Person classification (e.g., "main", "vicap", "ecap", "seeking-information")
        page_size: Number of results to return (default: 10, max: 50)
        
    Returns:
        A formatted string with search results matching the specified classification
    """
    try:
        url = "https://api.fbi.gov/wanted/v1/list"
        params = {
            'person_classification': classification.lower(),
            'pageSize': min(int(page_size), 50)
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if not data.get('items'):
            return f"No persons found with classification: {classification}"
        
        classification_descriptions = {
            'main': 'Main Wanted List',
            'vicap': 'Violent Criminal Apprehension Program',
            'ecap': 'Endangered Child Alert Program', 
            'seeking-information': 'Seeking Information Cases'
        }
        
        desc = classification_descriptions.get(classification.lower(), classification)
        result = f"🏷️ CLASSIFICATION: {desc.upper()}\n\n"
        
        for i, person in enumerate(data['items'], 1):
            name = person.get('title', 'Unknown')
            subjects = person.get('subjects', ['Unknown'])
            reward = person.get('reward_text', 'No reward specified')
            
            result += f"{i}. **{name}**\n"
            result += f"   Classification: {desc}\n"
            result += f"   Subjects: {', '.join(subjects)}\n"
            result += f"   Reward: {reward}\n"
            
            if person.get('description'):
                desc_text = person['description'][:150] + "..." if len(person['description']) > 150 else person['description']
                result += f"   Description: {desc_text}\n"
            
            result += "\n"
        
        result += f"Total results: {data.get('total', 'Unknown')} in classification '{classification}'"
        
        return result
        
    except Exception as e:
        return f"Error searching by classification '{classification}': {str(e)}"

def get_fbi_person_details(person_id: str) -> str:
    """Get comprehensive detailed information about a specific FBI wanted person by ID.
    
    Args:
        person_id: The unique ID of the person to get details for
        
    Returns:
        A formatted string with comprehensive detailed information about the person
    """
    try:
        # First try to get the person from the list since individual endpoint might not exist
        url = "https://api.fbi.gov/wanted/v1/list"
        params = {'pageSize': 50}  # Get more results to find the person
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        # Find the person by ID
        person = None
        for item in data.get('items', []):
            if item.get('uid') == person_id:
                person = item
                break
        
        if not person:
            return f"No person found with ID '{person_id}'"
        
        result = "📋 COMPREHENSIVE PERSON INFORMATION\n"
        result += "="*50 + "\n\n"
        
        # Basic identification
        result += "🆔 **IDENTIFICATION**\n"
        result += f"Name: {person.get('title', 'Unknown')}\n"
        result += f"ID: {person.get('uid', 'Unknown')}\n"
        
        aliases = person.get('aliases', [])
        if aliases:
            result += f"Aliases: {', '.join(aliases)}\n"
        
        # Status and classification
        status = person.get('status', 'na')
        status_icon = "🔴" if status == "na" else "🟢"
        status_text = "ACTIVE" if status == "na" else "CAPTURED"
        result += f"Status: {status_icon} {status_text}\n"
        
        poster_class = person.get('poster_classification', 'Unknown')
        person_class = person.get('person_classification', 'Unknown')
        result += f"Classification: {poster_class} / {person_class}\n\n"
        
        # Physical description
        result += "👤 **PHYSICAL DESCRIPTION**\n"
        sex = person.get('sex', 'Unknown')
        race = person.get('race_raw', person.get('race', 'Unknown'))
        result += f"Sex: {sex} | Race: {race}\n"
        
        # Height conversion
        height_min = person.get('height_min')
        height_max = person.get('height_max')
        if height_min:
            if height_max and height_max != height_min:
                height_str = f"{height_min//12}'{height_min%12}\" to {height_max//12}'{height_max%12}\""
            else:
                height_str = f"{height_min//12}'{height_min%12}\""
        else:
            height_str = "Unknown"
        
        weight = person.get('weight', 'Unknown')
        result += f"Height: {height_str} | Weight: {weight}\n"
        
        hair = person.get('hair_raw', person.get('hair', 'Unknown'))
        eyes = person.get('eyes_raw', person.get('eyes', 'Unknown'))
        result += f"Hair: {hair} | Eyes: {eyes}\n"
        
        complexion = person.get('complexion')
        build = person.get('build')
        if complexion or build:
            result += f"Complexion: {complexion or 'Not specified'} | Build: {build or 'Not specified'}\n"
        
        # Personal information
        result += "\n📋 **PERSONAL INFORMATION**\n"
        birth_dates = person.get('dates_of_birth_used', [])
        if birth_dates:
            result += f"Date(s) of Birth: {', '.join(birth_dates)}\n"
        
        birth_place = person.get('place_of_birth')
        if birth_place:
            result += f"Place of Birth: {birth_place}\n"
        
        nationality = person.get('nationality')
        if nationality:
            result += f"Nationality: {nationality}\n"
        
        age_range = person.get('age_range')
        if age_range:
            result += f"Age Range: {age_range}\n"
        
        # Occupations
        occupations = person.get('occupations', [])
        if occupations:
            result += f"Occupations: {', '.join(occupations)}\n"
        
        # Languages
        languages = person.get('languages', [])
        if languages:
            result += f"Languages: {', '.join(languages)}\n"
        
        # Distinguishing marks
        scars_marks = person.get('scars_and_marks')
        if scars_marks:
            result += f"\n🔍 **SCARS AND MARKS**\n{scars_marks}\n"
        
        # Criminal information
        result += "\n🚨 **CRIMINAL INFORMATION**\n"
        subjects = person.get('subjects', ['Unknown'])
        result += f"Subjects: {', '.join(subjects)}\n"
        
        description = person.get('description')
        if description:
            result += f"Charges: {description}\n"
        
        # Reward information
        reward = person.get('reward_text')
        if reward:
            result += f"Reward: {reward}\n"
        
        # Warning message
        warning = person.get('warning_message')
        if warning:
            result += f"\n⚠️ **WARNING**\n{warning}\n"
        
        # Case details
        if person.get('caution'):
            import re
            caution_clean = re.sub('<[^<]+?>', '', person['caution'])
            result += f"\n🚨 **CASE DETAILS**\n{caution_clean}\n"
        
        # Additional details
        if person.get('details'):
            import re
            details_clean = re.sub('<[^<]+?>', '', person['details'])
            result += f"\n📝 **ADDITIONAL DETAILS**\n{details_clean}\n"
        
        # Investigative information
        result += "\n🔍 **INVESTIGATIVE INFO**\n"
        field_offices = person.get('field_offices', [])
        if field_offices:
            result += f"Field Office(s): {', '.join(field_offices).title()}\n"
        
        publication = person.get('publication')
        if publication:
            result += f"Publication Date: {publication[:10]}\n"
        
        ncic = person.get('ncic')
        if ncic:
            result += f"NCIC Number: {ncic}\n"
        
        # Location information
        possible_countries = person.get('possible_countries', [])
        possible_states = person.get('possible_states', [])
        if possible_countries:
            result += f"Possible Countries: {', '.join(possible_countries)}\n"
        if possible_states:
            result += f"Possible States: {', '.join(possible_states)}\n"
        
        # Remarks
        if person.get('remarks'):
            import re
            remarks_clean = re.sub('<[^<]+?>', '', person['remarks'])
            result += f"\n💭 **REMARKS**\n{remarks_clean}\n"
        
        # Additional information
        if person.get('additional_information'):
            import re
            add_info_clean = re.sub('<[^<]+?>', '', person['additional_information'])
            result += f"\n📄 **ADDITIONAL INFORMATION**\n{add_info_clean}\n"
        
        # File and image availability
        images = person.get('images', [])
        files = person.get('files', [])
        if images or files:
            result += "\n📎 **AVAILABLE RESOURCES**\n"
            if images:
                result += f"Images Available: {len(images)} image(s)\n"
            if files:
                result += f"Files Available: {len(files)} file(s)\n"
        
        return result
        
    except Exception as e:
        return f"Error retrieving details for person ID '{person_id}': {str(e)}"

@tool
def get_fbi_terrorism_list() -> str:
    """Get the list of FBI's most wanted terrorists and terrorism-related persons.
    
    Returns:
        A formatted string with information about terrorism-related wanted persons
    """
    try:
        url = "https://api.fbi.gov/wanted/v1/list"
        params = {
            'pageSize': 20  # Get more results to filter terrorism cases
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if not data.get('items'):
            return "No persons found in the FBI database."
        
        # Filter for terrorism-related cases
        terrorism_keywords = ['terrorism', 'terrorist', 'seeking information - terrorism', 'counterterrorism']
        terrorism_cases = []
        
        for person in data['items']:
            subjects = person.get('subjects', [])
            for subject in subjects:
                if any(keyword.lower() in subject.lower() for keyword in terrorism_keywords):
                    terrorism_cases.append(person)
                    break
        
        if not terrorism_cases:
            return "No terrorism-related wanted persons found in current results."
        
        result = "🔴 FBI TERRORISM-RELATED CASES 🔴\n"
        result += "="*50 + "\n\n"
        
        for i, person in enumerate(terrorism_cases[:8], 1):
            name = person.get('title', 'Unknown')
            subjects = person.get('subjects', ['Unknown'])
            reward = person.get('reward_text', 'No reward specified')
            status = person.get('status', 'na')
            nationality = person.get('nationality', 'Unknown')
            field_offices = person.get('field_offices', [])
            
            # Status indicator
            status_icon = "🔴" if status == "na" else "🟢"
            status_text = "ACTIVE" if status == "na" else "CAPTURED"
            
            result += f"{i}. **{name}** {status_icon} {status_text}\n"
            result += f"   🏴 Nationality: {nationality}\n"
            result += f"   📂 Subjects: {', '.join(subjects)}\n"
            result += f"   💰 Reward: {reward}\n"
            
            if field_offices:
                result += f"   🏢 Field Office: {', '.join(field_offices).title()}\n"
            
            # Add warning if present
            if person.get('warning_message'):
                result += f"   ⚠️ WARNING: {person['warning_message']}\n"
            
            # Add occupation if available and relevant
            occupations = person.get('occupations', [])
            if occupations:
                result += f"   💼 Occupation: {', '.join(occupations)}\n"
            
            # Brief caution info
            if person.get('caution'):
                import re
                caution_clean = re.sub('<[^<]+?>', '', person['caution'])[:200] + "..."
                result += f"   🚨 Details: {caution_clean}\n"
            
            # Brief details
            elif person.get('details'):
                import re
                details_clean = re.sub('<[^<]+?>', '', person['details'])[:150] + "..."
                result += f"   📋 Details: {details_clean}\n"
            
            result += f"   🆔 ID: {person.get('uid', 'No ID')}\n\n"
        
        result += f"📊 Found {len(terrorism_cases)} terrorism-related case(s)\n"
        result += "⚠️ These cases involve national security matters"
        
        return result
        
    except Exception as e:
        return f"Error retrieving FBI terrorism-related cases: {str(e)}"

@tool
def get_fbi_by_poster_classification(classification: str = "default") -> str:
    """Get FBI wanted persons by poster classification type.
    
    Args:
        classification: Poster classification ("default", "law-enforcement-assistance", "missing", "information")
        
    Returns:
        A formatted string with search results matching the specified poster classification
    """
    try:
        url = "https://api.fbi.gov/wanted/v1/list"
        params = {
            'pageSize': 20,
            'sort_on': 'publication',
            'sort_order': 'desc'
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if not data.get('items'):
            return "No persons found in the FBI database."
        
        # Filter by poster classification
        filtered_items = [item for item in data['items'] if item.get('poster_classification', '').lower() == classification.lower()]
        
        if not filtered_items:
            return f"No persons found with poster classification: {classification}"
        
        classification_descriptions = {
            'default': 'Standard Wanted Persons',
            'law-enforcement-assistance': 'Law Enforcement Assistance Cases',
            'missing': 'Missing Persons Cases',
            'information': 'Seeking Information Cases'
        }
        
        desc = classification_descriptions.get(classification.lower(), classification)
        result = f"📋 {desc.upper()}\n"
        result += "="*50 + "\n\n"
        
        for i, person in enumerate(filtered_items[:10], 1):
            name = person.get('title', 'Unknown')
            subjects = person.get('subjects', ['Unknown'])
            status = person.get('status', 'na')
            reward = person.get('reward_text', 'No reward specified')
            publication = person.get('publication', 'Unknown date')[:10]
            field_offices = person.get('field_offices', [])
            
            # Status indicator
            status_icon = "🔴" if status == "na" else "🟢"
            status_text = "ACTIVE" if status == "na" else "CAPTURED"
            
            result += f"{i}. **{name}** {status_icon} {status_text}\n"
            result += f"   📂 Subjects: {', '.join(subjects)}\n"
            result += f"   💰 Reward: {reward}\n"
            result += f"   📅 Published: {publication}\n"
            
            if field_offices:
                result += f"   🏢 Field Office: {', '.join(field_offices).title()}\n"
            
            # Add warning if present
            if person.get('warning_message'):
                result += f"   ⚠️ WARNING: {person['warning_message']}\n"
            
            # Add age range for missing persons
            if person.get('age_range'):
                result += f"   👤 Age: {person['age_range']}\n"
            
            # Brief description
            if person.get('description'):
                desc_text = person['description'][:120] + "..." if len(person['description']) > 120 else person['description']
                result += f"   📋 Description: {desc_text}\n"
            
            result += f"   🆔 ID: {person.get('uid', 'No ID')}\n\n"
        
        result += f"📊 Found {len(filtered_items)} person(s) with classification '{classification}'\n"
        result += f"📄 Total in database: {data.get('total', 'Unknown')}"
        
        return result
        
    except Exception as e:
        return f"Error searching by poster classification '{classification}': {str(e)}"

# Create the string input tool versions for LangChain
search_fbi_by_field_office_tool = create_string_input_tool(search_fbi_by_field_office, "search_fbi_by_field_office")
search_fbi_by_status_tool = create_string_input_tool(search_fbi_by_status, "search_fbi_by_status")
search_fbi_by_classification_tool = create_string_input_tool(search_fbi_by_classification, "search_fbi_by_classification")
get_fbi_person_details_tool = create_string_input_tool(get_fbi_person_details, "get_fbi_person_details")

@tool
def get_fbi_advanced_search(title: str = "", sort_criteria: str = "publication") -> str:
    """Advanced FBI search with title filtering and sorting options.
    
    Args:
        title: Part of the person's name to search for (optional)
        sort_criteria: How to sort results (publication, title, subjects)
        
    Returns:
        A formatted string with advanced search results
    """
    try:
        url = "https://api.fbi.gov/wanted/v1/list"
        params = {
            'pageSize': 15,
            'sort_on': sort_criteria.lower(),
            'sort_order': 'desc'
        }
        
        # Add title filter if provided
        if title.strip():
            params['title'] = title.strip()
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if not data.get('items'):
            search_term = f" for '{title}'" if title else ""
            return f"No wanted persons found{search_term} with current search criteria."
        
        search_info = f" matching '{title}'" if title else ""
        result = f"🔍 ADVANCED SEARCH RESULTS{search_info.upper()}\n"
        result += f"Sorted by: {sort_criteria}\n\n"
        
        for i, person in enumerate(data['items'], 1):
            name = person.get('title', 'Unknown')
            subjects = person.get('subjects', ['Unknown'])
            reward = person.get('reward_text', 'No reward specified')
            publication = person.get('publication', 'Unknown date')
            uid = person.get('uid', 'No ID')
            
            result += f"{i}. **{name}** (ID: {uid})\n"
            result += f"   Subjects: {', '.join(subjects)}\n"
            result += f"   Reward: {reward}\n"
            result += f"   Publication: {publication}\n"
            
            # Add warning info if available
            if person.get('warning_message'):
                result += f"   ⚠️ Warning: {person['warning_message']}\n"
            
            if person.get('description'):
                desc = person['description'][:120] + "..." if len(person['description']) > 120 else person['description']
                result += f"   Description: {desc}\n"
            
            result += "\n"
        
        result += f"Total available: {data.get('total', 'Unknown')} results"
        result += f"\nSorted by: {sort_criteria} (descending order)"
        
        return result
        
    except Exception as e:
        return f"Error in advanced search: {str(e)}"