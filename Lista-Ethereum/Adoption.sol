pragma solidity ^0.4.17;

/* TODO: Final do contrato enviar ether pra sua conta */

contract Adoption {
    
  event PetComprado(address comprador, uint valor);
  event PetReembolso(address comprator, uint valor);

  enum STATUSPET {A_VENDA, VENDIDO}
  STATUSPET statuspet;
  
  address owner;
  
  struct Pet {
	bytes name;
	address adopter;
	uint preco;
	STATUSPET _status;
  }

  Pet[] public pets;
  
  /* Valor minimo de um pet */
  uint min_preco = 2;

  constructor() public {
      owner = msg.sender;
  }

  function addPet(bytes name) public returns (uint) {
      require(owner == msg.sender) ;
	  
	  Pet memory newPet = Pet(name, address(0), min_preco, STATUSPET.A_VENDA);

	  pets.push(newPet);
	
      return pets.length - 1;
  }
  
  function getAddr() public view returns (address) {
      return owner;
  }
  
  function setValorMinPreco(uint _min_preco) public returns (uint) {
      require(owner == msg.sender) ;
            
      min_preco = _min_preco;
      
      return min_preco;
  }

  function getNumberOfPets() public view returns (uint) {
	return pets.length;
  }

  modifier validPet(uint petId) {
	require(petId >= 0 && petId < pets.length) ;
	_;
  }

  function getPet(uint petId)
	validPet(petId)
	public
	view
	returns(bytes, address)
	{
		return (pets[petId].name, pets[petId].adopter);
	}

   function adopt(uint petId, uint value)
	validPet(petId)
	public
	payable
	returns(uint)
	{
	    require(value == msg.value);
	    require(value > min_preco);

		Pet storage pet = pets[petId];
		
		/* Devolve dinheiro. TODO: caso de erro */
		if(pet._status == STATUSPET.VENDIDO) {
		    msg.sender.transfer(value);
		    
		    emit PetReembolso(msg.sender, value);
		} else {
			pet.adopter = msg.sender ;
			pet._status = STATUSPET.VENDIDO;
			pet.preco = msg.value;
		    pets[petId] = pet;
		    
		    emit PetComprado(msg.sender, value) ;
		    
		    return petId;
		}
	}
	
	/* Destroi o contrato e envia o balanco de ethers para o dono */
	function killPetshop() public {
	    require(owner == msg.sender);
	    
        selfdestruct(owner);
        
	}
}
