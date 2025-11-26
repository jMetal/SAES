from SAES.statistical_tests.bayesian import bayesian_sign_test, bayesian_signed_rank_test
import pandas as pd
import numpy as np
import unittest


class TestBayesianTests(unittest.TestCase):
    """Test suite for Bayesian statistical tests."""
    
    def setUp(self):
        """Set up test fixtures with various data scenarios."""
        
        # Data where algorithm A is clearly better
        self.data_a_better = pd.DataFrame({
            "Algorithm_A": [0.9, 0.85, 0.95, 0.9, 0.92, 0.88, 0.91, 0.89],
            "Algorithm_B": [0.5, 0.6, 0.55, 0.58, 0.52, 0.54, 0.56, 0.57]
        })
        
        # Data where algorithms are equivalent
        self.data_equivalent = pd.DataFrame({
            "Algorithm_A": [0.5, 0.6, 0.7, 0.55, 0.65],
            "Algorithm_B": [0.5, 0.6, 0.7, 0.55, 0.65]
        })
        
        # Data with small differences (within ROPE)
        self.data_rope = pd.DataFrame({
            "Algorithm_A": [0.500, 0.505, 0.498, 0.502, 0.501],
            "Algorithm_B": [0.501, 0.504, 0.499, 0.503, 0.500]
        })
        
        # Data where algorithm B is clearly better
        self.data_b_better = pd.DataFrame({
            "Algorithm_A": [0.5, 0.6, 0.55, 0.58, 0.52],
            "Algorithm_B": [0.9, 0.85, 0.95, 0.9, 0.92]
        })

    def test_bayesian_sign_test_basic(self):
        """Test basic functionality of bayesian_sign_test."""
        result, samples = bayesian_sign_test(self.data_a_better)
        
        # Check return types
        self.assertIsInstance(result, np.ndarray)
        self.assertIsInstance(samples, np.ndarray)
        
        # Check result shape (should be 3 probabilities)
        self.assertEqual(result.shape, (3,))
        
        # Check probabilities sum to 1
        self.assertAlmostEqual(np.sum(result), 1.0, places=5)
        
        # Check all probabilities are between 0 and 1
        self.assertTrue(np.all(result >= 0) and np.all(result <= 1))

    def test_bayesian_sign_test_a_better(self):
        """Test bayesian_sign_test when algorithm A is clearly better."""
        result, _ = bayesian_sign_test(self.data_a_better, sample_size=2500)
        
        # Algorithm A should have high probability of being better (result[2] should be high)
        self.assertGreater(result[2], 0.5, 
                          "Algorithm A should have >50% probability of being better")

    def test_bayesian_sign_test_equivalent(self):
        """Test bayesian_sign_test when algorithms are equivalent."""
        result, _ = bayesian_sign_test(self.data_equivalent, sample_size=2500)
        
        # Rope probability should be highest for equivalent algorithms
        self.assertGreater(result[1], result[0], 
                          "Rope probability should be higher than left")
        self.assertGreater(result[1], result[2], 
                          "Rope probability should be higher than right")

    def test_bayesian_sign_test_custom_rope(self):
        """Test bayesian_sign_test with custom ROPE limits."""
        result, _ = bayesian_sign_test(
            self.data_rope, 
            rope_limits=[-0.1, 0.1],
            sample_size=2500
        )
        
        # With wide ROPE, should classify as equivalent
        self.assertGreater(result[1], 0.3, 
                          "With wide ROPE, rope probability should be significant")

    def test_bayesian_sign_test_prior_strength(self):
        """Test bayesian_sign_test with different prior strengths."""
        result_weak, _ = bayesian_sign_test(
            self.data_a_better, 
            prior_strength=0.1,
            sample_size=2500
        )
        result_strong, _ = bayesian_sign_test(
            self.data_a_better, 
            prior_strength=5.0,
            sample_size=2500
        )
        
        # Both should still identify A as better, but with different confidence
        self.assertGreater(result_weak[2], result_strong[2],
                          "Weaker prior should allow stronger data influence")

    def test_bayesian_sign_test_prior_place(self):
        """Test bayesian_sign_test with different prior placements."""
        for prior_place in ["left", "rope", "right"]:
            result, _ = bayesian_sign_test(
                self.data_a_better,
                prior_place=prior_place,
                sample_size=1000
            )
            # Should still work and return valid probabilities
            self.assertAlmostEqual(np.sum(result), 1.0, places=5)

    def test_bayesian_sign_test_invalid_prior_strength(self):
        """Test bayesian_sign_test with invalid prior strength."""
        with self.assertRaises(ValueError):
            bayesian_sign_test(self.data_a_better, prior_strength=0)
        
        with self.assertRaises(ValueError):
            bayesian_sign_test(self.data_a_better, prior_strength=-1)

    def test_bayesian_sign_test_invalid_prior_place(self):
        """Test bayesian_sign_test with invalid prior place."""
        with self.assertRaises(ValueError):
            bayesian_sign_test(self.data_a_better, prior_place="invalid")

    def test_bayesian_sign_test_invalid_data_shape(self):
        """Test bayesian_sign_test with invalid data shape."""
        invalid_data = pd.DataFrame({
            "A": [1, 2, 3],
            "B": [4, 5, 6],
            "C": [7, 8, 9]
        })
        
        with self.assertRaises(ValueError):
            bayesian_sign_test(invalid_data)

    def test_bayesian_signed_rank_test_basic(self):
        """Test basic functionality of bayesian_signed_rank_test."""
        result, samples = bayesian_signed_rank_test(self.data_a_better, sample_size=500)
        
        # Check return types
        self.assertIsInstance(result, np.ndarray)
        self.assertIsInstance(samples, np.ndarray)
        
        # Check result shape
        self.assertEqual(result.shape, (3,))
        
        # Check probabilities sum to 1
        self.assertAlmostEqual(np.sum(result), 1.0, places=5)
        
        # Check all probabilities are between 0 and 1
        self.assertTrue(np.all(result >= 0) and np.all(result <= 1))

    def test_bayesian_signed_rank_test_a_better(self):
        """Test bayesian_signed_rank_test when algorithm A is clearly better."""
        result, _ = bayesian_signed_rank_test(self.data_a_better, sample_size=500)
        
        # Algorithm A should have high probability of being better
        self.assertGreater(result[2], 0.5,
                          "Algorithm A should have >50% probability of being better")

    def test_bayesian_signed_rank_test_equivalent(self):
        """Test bayesian_signed_rank_test when algorithms are equivalent."""
        result, _ = bayesian_signed_rank_test(self.data_equivalent, sample_size=500)
        
        # Rope probability should be highest
        self.assertGreater(result[1], 0.3,
                          "Rope probability should be significant for equivalent algorithms")

    def test_bayesian_signed_rank_test_invalid_prior_strength(self):
        """Test bayesian_signed_rank_test with invalid prior strength."""
        with self.assertRaises(ValueError):
            bayesian_signed_rank_test(self.data_a_better, prior_strength=0)

    def test_bayesian_signed_rank_test_invalid_prior_place(self):
        """Test bayesian_signed_rank_test with invalid prior place."""
        with self.assertRaises(ValueError):
            bayesian_signed_rank_test(self.data_a_better, prior_place="invalid")

    def test_bayesian_signed_rank_test_invalid_data_shape(self):
        """Test bayesian_signed_rank_test with invalid data shape."""
        invalid_data = pd.DataFrame({
            "A": [1, 2],
            "B": [4, 5],
            "C": [7, 8]
        })
        
        with self.assertRaises(ValueError):
            bayesian_signed_rank_test(invalid_data)

    def test_bayesian_tests_with_numpy_array(self):
        """Test that both functions work with numpy arrays."""
        data_array = self.data_a_better.values
        
        result_sign, _ = bayesian_sign_test(data_array, sample_size=1000)
        result_rank, _ = bayesian_signed_rank_test(data_array, sample_size=500)
        
        # Both should return valid probabilities
        self.assertAlmostEqual(np.sum(result_sign), 1.0, places=5)
        self.assertAlmostEqual(np.sum(result_rank), 1.0, places=5)

    def test_bayesian_tests_reproducibility(self):
        """Test that setting random seed produces consistent results."""
        np.random.seed(42)
        result1, _ = bayesian_sign_test(self.data_a_better, sample_size=1000)
        
        np.random.seed(42)
        result2, _ = bayesian_sign_test(self.data_a_better, sample_size=1000)
        
        # Results should be identical with same seed
        np.testing.assert_array_almost_equal(result1, result2, decimal=10)

    def test_bayesian_sample_size_effect(self):
        """Test that larger sample sizes give more stable results."""
        result_small, _ = bayesian_sign_test(self.data_a_better, sample_size=100)
        result_large, _ = bayesian_sign_test(self.data_a_better, sample_size=5000)
        
        # Both should identify the same winner, but may have different confidence
        winner_small = np.argmax(result_small)
        winner_large = np.argmax(result_large)
        self.assertEqual(winner_small, winner_large,
                        "Both sample sizes should identify the same winner")


if __name__ == '__main__':
    unittest.main()

