# dungeon-art

## Purpose
Provide verified dungeon-art behavior for the cooperative Gauntlet-inspired 3D dungeon game.

## Requirements

### Requirement: Original 3D asset set
The game SHALL display original Blender-created 3D geometry for four heroes, four enemies and a coherent dungeon kit.

#### Scenario: Original 3D asset set acceptance
- **WHEN** the player views the dungeon from above
- **THEN** class silhouettes and enemy types are identifiable with distinct player rings

### Requirement: Editable exports
Assets SHALL include editable source, export provenance, structural checks and actual preview evidence.

#### Scenario: Editable exports acceptance
- **WHEN** exports are loaded in the browser
- **THEN** geometry materials and scale match their source
