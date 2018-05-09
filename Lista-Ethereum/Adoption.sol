pragma solidity ^0.4.17;

/*
    Lista solidity
    Aluno: Marcos Paulo Ferreira
*/

contract Adoption {
    
  event PetComprado(uint idCompra, string nome, address comprador, uint valor);
  //event RemovendoCompra(uint idCompra, address comprador, uint valor) ;
  event PetJaComDono(uint petId, address comprador_original, address comprador_negado);
  event Reembolso(address comprador, uint valor);

  enum STATUSPET {A_VENDA, VENDIDO}
  STATUSPET statuspet;
  
  address public owner;
  
  struct Pet {
	string name;
	address adopter;
	uint preco;
	STATUSPET _status;
  }
  
  struct Comprador {
      /* endereço */
      address endereco;
      /* valor recebido */
      uint valor;
  }

  /* mapeia id de um pet a uma lista de compradores */
  mapping(uint => Comprador[]) compras;

  Pet[] public pets;
  
  constructor() public {
      owner = msg.sender;
  }

  function addPet(string name) public returns (uint) {
      require(owner == msg.sender) ;
	  
	  Pet memory newPet = Pet(name, address(0), 0, STATUSPET.A_VENDA);

	  pets.push(newPet);
	
      return pets.length - 1;
  }

  function getNumberOfPets() public view returns (uint)
  {
	return pets.length;
  }

  modifier validPet(uint petId)
  {
	require(petId >= 0 && petId < pets.length) ;
	_;
  }
  
  modifier validCompra(uint petId, uint index)
  {
      require(petId >= 0 && petId < pets.length) ;
      require(index >= 0 && index < compras[petId].length);
      _;
  }
  
  function getCompraMaisCaraPet(uint petId)
  public
  view
  returns(uint, uint)
  {
      uint maior_indice = 0;
      uint maior_valor = 0;
      for(uint index = 0; index < compras[petId].length; index++)
      {
          if (maior_valor < compras[petId][index].valor)
          {
              maior_valor = compras[petId][index].valor;
              maior_indice = index;
          }
       }
       
      return (maior_indice, maior_valor);
  }
  
  function getPetStatus(uint petId)
  validPet(petId)
  public
  view
  returns(string)
  {
      if(pets[petId]._status == STATUSPET.VENDIDO) return "vendido";
      else return "disponivel";
  }

  function getPet(uint petId)
	validPet(petId)
	public
	view
	returns(string, address, uint, STATUSPET)
	{
		return (pets[petId].name, pets[petId].adopter, pets[petId].preco, pets[petId]._status);
	}
	
   /* Funcao de adocao. Aceita o id do pet e o valor */
   function adopt(uint petId, uint value)
	validPet(petId)
	public
	payable
	returns(address, uint)
	{
	    require(value == msg.value);
	    
		Pet storage pet = pets[petId];

		if(pet._status == STATUSPET.A_VENDA) {
	        Comprador memory c = Comprador(msg.sender, msg.value) ;
	        
	        c.endereco = msg.sender;
	        c.valor = msg.value;

		    compras[petId].push(c);
		    
		    return (c.endereco, c.valor);
		} else { /* Pet ja vendido mas recebeu proposta de compra */
		    emit PetJaComDono(petId, pets[petId].adopter, msg.sender) ;
		}
		
		/* retorno para fins de Debug */
		return (address(0), 0);
	}

    /* Chamado pelo dono do contrato. Finaliza a compra de um Pet */
	function aceitaCompraPet(uint petId, uint index)
	validCompra(petId, index)
	public
	{
	    require(owner == msg.sender);

	    address endereco;
	    uint valor;
	
	    /* Remove a compra e devolve o dinheiro */
	    for(uint i=0; i < compras[petId].length; i++)
	    {
	        if(i != index ) {
	            endereco = compras[petId][i].endereco;
	            valor    = compras[petId][i].valor;
	            
	            //emit RemovendoCompra(i, endereco, valor);
	            
	            emit Reembolso(endereco, valor);
	            /* TODO: Verificar metodo melhor pra evitar reentrancy */
	            if(valor > 0)
	            {
	                endereco.transfer(valor);
	                /* Evita reenvio por reentrada */
	                compras[petId][i].valor = 0;
	            }
	        }
	    }
	    
	    pets[petId]._status = STATUSPET.VENDIDO;
	    pets[petId].adopter = compras[petId][index].endereco;
	    pets[petId].preco = compras[petId][index].valor;
	    
	    emit PetComprado(index, pets[petId].name, pets[petId].adopter, pets[petId].preco) ;
	    
	    delete compras[petId];
	}

    /* Total de pedidos de um Pet */
	function getTotalComprasByPet(uint petId)
	public
	view
	returns(uint)
	{
	    return compras[petId].length;
	}
	
	/* Obtem uma compra/pedido. Exemplo: pedido 1 do pet 0, logo parametro: (0, 1) */
	function getCompraPet(uint petId, uint index)
	validCompra(petId, index)
	public
	view
	returns(address, uint)
	{
	    return (compras[petId][index].endereco, compras[petId][index].valor);
	}
	
	/* Destroi o contrato e envia o balanco de ethers para o dono */
	function killPetshop()
	public
	{
	    require(owner == msg.sender);
	    
        selfdestruct(owner);
	}
}
