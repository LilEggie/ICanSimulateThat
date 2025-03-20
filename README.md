# ICanSimulateThat

## Overview
**ICanSimulateThat** is a simulation project designed to model the process of completing a collection in *TCG Card Shop Simulator*. By simulating card pack openings, drop rates, and collection progress, this project provides insights into the probability and effort required to complete a full set of cards.

## Features
- **Pack Opening Simulation** – Emulates opening card packs with predefined drop rates.
- **Collection Tracking** – Keeps track of owned and missing cards in a collection.
- **Probability Analysis** – Estimates the number of packs needed to complete a set.
- **Customizable Settings** – Adjust card rarity, drop rates, and collection goals.
- **Efficient Simulation** – Runs thousands of simulations quickly to provide statistical insights.

## Installation & Usage

### Cloning the Repository
To get started, clone the repository using:
```sh
git clone https://github.com/yourusername/ICanSimulateThat.git
cd ICanSimulateThat
```

### Running the Simulation
```sh
python -m icst.main
```

## Customization
Configuring cards, packs, and expansions will be done in their respective folders in the resources directory.
- The `cards` directory for the cards
- The `packs` directory for the packs
- The `expansions` directory for the expansions

### Modifying Border Drop Rates
To adjust border drop rates, navigate to the `cards` directory and open the JSON file for the card type you want to modify.

In the `"border_chances"` section, you can update the floating-point values to set the probability of a card having a specific border. The values represent percentages (e.g., 21.5 means a 21.5% chance).

You can also add new border types. For example, to introduce "shiny" and "sparkly" borders, modify the JSON file as follows. If you add new border types, make sure you do exactly the same thing—name and order—in the corresponding expansion JSON files.
```json
"border_chances": {
  "shiny": 1.0,
  "sparkly": 5.0,
}
```

**Important Notes**
- **Order matters**: The program determines the card's border sequentially. In the example above, it first checks if the card is "shiny," then "sparkly."
- **Ensure a guaranteed border exists**: At least one border must have a 100% drop rate. Otherwise, the program may generate a card without a border, potentially causing errors.

### Modifying Cards
The `cards` directory contains multiple JSON files, each defining a specific card type within an expansion. Below is a template for a card JSON file:
```json
{
    "expansion": "base_common",

    "foil_chance": 5.0,

    "border_chances": {
        "full_art": 0.25,
        "ex": 1.0,
        "gold": 4.0,
        "silver": 8.0,
        "first_edition": 20.0,
        "basic": 100.0
    }
}
```
- `expansion`: Specifies the expansion set the card belongs to. The name should match corresponding folder structure (`base_common` → `base/common.json`).
- `foil_chance`: Probability (in percentage) that the card is a foil card.
- `border_chances`: Defines possible borders and their drop rates. **Ensure these match the `border` section exactly—name and order—in the corresponding expansion JSON files.**

**When adding new cards, make sure the corresponding expansion directory contains a matching JSON file.** If you create a `base/common.json` file, an equivalent `base/common.json` file should exist in the `expansions` directory.

### Modifying Expansions
The `expansions` directory contains JSON files defining each expansion and its card list. Below is a template for an expansion JSON file:
```json
{
    "borders": [
        "basic",
        "first_edition",
        "silver",
        "gold",
        "ex",
        "full_art"
    ],

    "cards": [
        "Pigni", "Kidsune", "Nanomite", "Sapoling", "Minstar", 
        "Shellow", "Wurmgle", "Nocti", "Helio", "Werboo",
        "Flami", "Kyrone", "Lupup", "Gupi", "Batrang",
        "Tetron", "Clawop", "Sunflork", "Crobib", "Nimblis",
        "Esmeri", "Seedant", "Mufflin", "Anguifish"
    ]
}
```
- `borders`: Lists all valid borders for this expansion. **Ensure these match the `border_chances` section exactly—name and order—in the corresponding card JSON files.**
- `cards`: Lists all card names available in the expansion.

### Modifying Packs
The `packs` directory contains JSON files defining pack contents and dop rates. Below is a template for a pack JSON file:
```json
{
    "base_common": 6,
    "*": {
        "ghost": 0.1,
        "base_common": 100.0
    }
}
```

In this example, there are 6 guaranteed base common cards, indicated as `"base_common": 6`. When adding cards to a pack, make sure the name match the corresponding card folder structure (`base_common` → `base/common.json`).

Additionally, the example pack contains a wildcard slot, indicated as `*`. All keys that start with '*' will be considered wildcards. Wildcard slots will randomly choose a card based on their assigned probabilities. In the example above, there is a 0.1% chance of the card being a ghost card. Otherwise, it will be a base common card. **Ensure that every wildcard slot contains a guaranteed (100%) card type.**

## Future Enhancements
- **Importing World Files**: Simulate completing a player's collection in a given world.
- **GUI Integration**: Add a visual representation of collection progress and statistics.
