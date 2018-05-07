pragma solidity ^0.4.17;

import "truffle/Assert.sol";
import "truffle/DeployedAddresses.sol";
import "./ThrowProxy.sol";
import "../contracts/Adoption.sol";

contract TestAdoption {
	Adoption adoption = Adoption(DeployedAddresses.Adoption());
	ThrowProxy throwProxy = new ThrowProxy(address(adoption)) ;
	Adoption throwableAdoption = Adoption(address(throwProxy));

	function testUserCanAddPet() public {
		uint returnedId = adoption.addPet("Dog Test");
		uint expected = 0;

		Assert.equal(returnedId, expected, "pet ID 0 should be recorded.") ;
	}

	function testUserCanGetTheNumberOfPets() public {
		uint expectedPetLength = 1;
		uint petLength = adoption.getNumberOfPets();

		Assert.equal(petLength, expectedPetLength, "Numer of pets should be 1.") ;
	}

	function testUserCanGetPet() public {
		address expectedAdopter = address(0) ;
		var (,adopter) = adoption.getPet(0);

		Assert.equal(adopter, expectedAdopter, "Adopter of pet ID 0 should be empty.") ;
	}

	function testUserCannotGetAnInvalidPet() public {
		//throwableAdoption.getPet(1) ;
		//throwProxy.shouldThrow();
		address(throwableAdoption).call(abi.encodeWithSignature("getPet(unit)", uint(1)));
		throwProxy.shouldThrow() ;
	}

	function testUserCanAdoptPet() public {
		uint returnedId = adoption.adopt(0);
		uint expectedId = 0;

		address expectedAdopter = this;
		Assert.equal(returnedId, expectedId, "Adoption of pet ID 0 should be recorded.");
		var (, adopter) = adoption.getPet(0);

		Assert.equal(adopter, expectedAdopter, "Adopter of pet ID 0 should be the TestAdoption contract.") ;

	}

	function testUserCannotAdoptAnInvalidPet() public {
		//throwableAdoption.adopt(1);
		//throwProxy.shouldThrow();
		address(throwableAdoption).call(abi.encodeWithSignature("adopt(uint)", uint(1)));
		throwProxy.shouldThrow();
	}
}
