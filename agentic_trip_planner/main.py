from crew import ResearchCrew


def save_to_file(data, filename):
    """Save the given data to a file."""
    with open(filename, 'w') as file:
        file.write(data)


def main():
    research_crew = ResearchCrew()

    result = research_crew.crew().kickoff(
        inputs={'area': 'Wellington New Zealand', 'interest': 'outdoor activities'}
    )
    save_to_file(result.raw, 'agentic_trip_planner/outputs/output_quen.md')


if __name__ == '__main__':
    main()
