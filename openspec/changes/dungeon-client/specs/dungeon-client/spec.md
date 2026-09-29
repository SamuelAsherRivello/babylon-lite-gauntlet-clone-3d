# Spec Delta

## Purpose
Provide verified dungeon-client behavior for the cooperative Gauntlet-inspired 3D dungeon game.

## ADDED Requirements

### Requirement: Play and switch
The client SHALL hot join, show four instant class buttons and retain distinct connection colors for duplicate classes.

#### Scenario: Play and switch acceptance
- **WHEN** two players choose wizard
- **THEN** both see separate colored numbered identities and synchronized world state

### Requirement: Controls and recovery
The client SHALL support keyboard and simultaneous touch movement/attack, safe blur/cancel release, local pause and connection/unsupported states.

#### Scenario: Controls and recovery acceptance
- **WHEN** focus is lost or a touch is canceled
- **THEN** input stops without pausing other players

### Requirement: Public delivery
The game SHALL provide one complete playable dungeon on GitHub Pages with version, instructions, documentation and verified desktop/mobile presentation.

#### Scenario: Public delivery acceptance
- **WHEN** two independent clients join the public game
- **THEN** both can play the same released level
