"""
DemCoin Game Theory Simulator
Predicts citizen behavior under different parameter settings
"""

import random
from typing import List, Dict

class DemCoinSimulator:
    """
    Simulates citizen participation in democratic processes
    under the DemCoin incentive mechanism
    """
    
    def __init__(
        self,
        num_citizens: int = 10000,
        demcoin_per_hour: float = 15.0,
        success_bonus: float = 100.0,
        time_cost: float = 3.0,
        quality_threshold: float = 7.0
    ):
        self.num_citizens = num_citizens
        self.demcoin_per_hour = demcoin_per_hour
        self.success_bonus = success_bonus
        self.time_cost = time_cost
        self.quality_threshold = quality_threshold
        
        # Citizen attributes (simplified)
        self.citizens = self._initialize_citizens()
    
    def _initialize_citizens(self) -> List[Dict]:
        """Create diverse citizen population"""
        citizens = []
        for i in range(self.num_citizens):
            citizen = {
                'id': i,
                'skill': random.uniform(0.5, 1.5),  # Quality multiplier
                'time_value': random.uniform(10, 50),  # €/hour they value their time
                'civic_interest': random.uniform(0, 1)  # How much they care
            }
            citizens.append(citizen)
        return citizens
    
    def calculate_utility_study(self, citizen: Dict, participation_rate: float) -> float:
        """
        Calculate expected utility if citizen studies
        """
        # Immediate reward for quality work
        quality_score = citizen['skill'] * 8  # Base quality
        if quality_score >= self.quality_threshold:
            immediate_reward = self.demcoin_per_hour * self.time_cost
        else:
            immediate_reward = 0
        
        # Expected success bonus
        # More participants → higher quality decisions → more likely to succeed
        prob_success = 0.3 + (participation_rate * 0.6)  # 30% base, up to 90%
        expected_bonus = prob_success * self.success_bonus
        
        # Time cost
        time_cost_euros = citizen['time_value'] * self.time_cost
        
        # Total utility
        total_utility = immediate_reward + expected_bonus - time_cost_euros
        
        # Civic interest adds intrinsic motivation
        total_utility += citizen['civic_interest'] * 20
        
        return total_utility
    
    def calculate_utility_ignore(self, citizen: Dict) -> float:
        """
        Calculate expected utility if citizen ignores
        """
        # Save time but get nothing
        return 0
    
    def simulate_one_round(self) -> Dict:
        """
        Simulate one round of decision-making
        Find Nash equilibrium through iteration
        """
        # Start with assumption: nobody participates
        participation_rate = 0.0
        participating = [False] * self.num_citizens
        
        # Iterate until stable (Nash equilibrium)
        max_iterations = 20
        for iteration in range(max_iterations):
            changed = False
            
            for i, citizen in enumerate(self.citizens):
                # Calculate utilities under current participation rate
                utility_study = self.calculate_utility_study(citizen, participation_rate)
                utility_ignore = self.calculate_utility_ignore(citizen)
                
                # Choose best strategy
                should_participate = utility_study > utility_ignore
                
                if should_participate != participating[i]:
                    participating[i] = should_participate
                    changed = True
            
            # Update participation rate
            new_rate = sum(participating) / self.num_citizens
            
            # Check convergence
            if abs(new_rate - participation_rate) < 0.001:
                participation_rate = new_rate
                break
            
            participation_rate = new_rate
        
        # Calculate results
        num_participating = sum(participating)
        avg_quality = sum(
            citizen['skill'] * 8 
            for i, citizen in enumerate(self.citizens) 
            if participating[i]
        ) / max(num_participating, 1)
        
        return {
            'participation_rate': participation_rate * 100,
            'num_participating': num_participating,
            'avg_quality': avg_quality,
            'converged_iteration': iteration + 1
        }
    
    def optimize_parameters(self) -> Dict:
        """
        Find optimal parameter settings
        """
        best_params = None
        best_score = -float('inf')
        
        # Try different parameter combinations
        for demcoin_rate in [10, 15, 20, 25]:
            for bonus in [50, 100, 150, 200]:
                # Test these parameters
                self.demcoin_per_hour = demcoin_rate
                self.success_bonus = bonus
                
                result = self.simulate_one_round()
                
                # Score = participation * quality - cost
                cost = result['num_participating'] * self.time_cost * demcoin_rate
                score = result['participation_rate'] * result['avg_quality'] - cost / 1000
                
                if score > best_score:
                    best_score = score
                    best_params = {
                        'demcoin_per_hour': demcoin_rate,
                        'success_bonus': bonus,
                        'result': result
                    }
        
        return best_params


# Example usage
if __name__ == "__main__":
    print("🎯 DemCoin Game Theory Simulator\n")
    
    # Create simulator
    sim = DemCoinSimulator(
        num_citizens=1000,  # Small test
        demcoin_per_hour=15,
        success_bonus=100,
        time_cost=3
    )
    
    print("Running simulation...")
    result = sim.simulate_one_round()
    
    print(f"\n📊 Results:")
    print(f"  Participation Rate: {result['participation_rate']:.1f}%")
    print(f"  Number Participating: {result['num_participating']}")
    print(f"  Average Quality: {result['avg_quality']:.1f}/10")
    print(f"  Converged after {result['converged_iteration']} iterations")
    
    print("\n🔧 Finding optimal parameters...")
    optimal = sim.optimize_parameters()
    print(f"\n✨ Optimal Settings:")
    print(f"  DemCoin per hour: {optimal['demcoin_per_hour']}")
    print(f"  Success bonus: {optimal['success_bonus']}")
    print(f"  Expected participation: {optimal['result']['participation_rate']:.1f}%")
