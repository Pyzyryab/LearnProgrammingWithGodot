//! Contains the ROOT elements of the project, which are the components and
//! bindings for the base of all nodes in our games hierarchy

use godot::{bind::{GodotClass, godot_api}, engine::{INode, Node, load, PackedScene, PackedSceneExt}, obj::Base, log::godot_print};

use crate::player::PlayerCharacter;

#[derive(GodotClass)]
#[class(base=Node)]
pub struct Game {
    #[export] development_mode: bool,
    #[base] game: Base<Node>
}

#[godot_api]
impl INode for Game {
    fn init(game: Base<Node>) -> Self {
        godot_print!("Game initialized");
        
        Self {
            development_mode: true,
            game
        }
    }

    fn ready(&mut self) {
        let player_character_scene = load::<PackedScene>("res://scenes/player.tscn")
            .instantiate_as::<PlayerCharacter>()
            .upcast::<Node>();
        self.game.add_child(player_character_scene);

        for child in self.game.get_children().iter_shared() {
            let c = child.get_name();
            godot_print!("Child name: {:?}", c);
        }
        
        godot_print!("Game ready");
    }
}
