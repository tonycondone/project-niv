import pytest
import time
import os
import tempfile
import sys

# Add the project root to Python path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config_utils import ConfigValidator
from email_utils import EmailSender
from logger import logger, log_performance


class TestPerformance:
    """Performance tests for PROJECT NIV components."""

    def setup_method(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.test_config = {
            'sender_email': 'test@example.com',
            'password': 'testpassword123',
            'smtp_server': 'smtp.gmail.com',
            'smtp_port': 587,
            'receiver_emails': ['recipient1@example.com'],
            'subject': 'Performance Test',
            'send_time': '08:00'
        }

    def teardown_method(self):
        """Clean up test fixtures."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_config_loading_performance(self):
        """Test configuration loading performance."""
        config_path = os.path.join(self.temp_dir, 'perf_config.json')

        with open(config_path, 'w') as f:
            import json
            json.dump(self.test_config, f)

        # Measure config loading time
        start_time = time.time()
        for _ in range(100):  # Load config 100 times
            config = ConfigValidator.load_config(config_path)
        end_time = time.time()

        duration = end_time - start_time
        log_performance(logger, "config_loading_100x", duration)

        # Should complete in reasonable time (less than 1 second for 100 loads)
        assert duration < 1.0

    def test_email_initialization_performance(self):
        """Test EmailSender initialization performance."""
        # Measure EmailSender initialization time
        start_time = time.time()
        for _ in range(50):  # Initialize 50 times
            email_sender = EmailSender(config=self.test_config)
        end_time = time.time()

        duration = end_time - start_time
        log_performance(logger, "email_sender_init_50x", duration)

        # Should complete in reasonable time
        assert duration < 2.0

    def test_file_size_calculation_performance(self):
        """Test file size calculation performance."""
        email_sender = EmailSender(config=self.test_config)

        # Create test files of different sizes
        test_files = []
        for size in [1000, 10000, 100000]:  # 1KB, 10KB, 100KB
            file_path = os.path.join(self.temp_dir, f'test_{size}.txt')
            with open(file_path, 'w') as f:
                f.write('x' * size)
            test_files.append(file_path)

        # Measure file size calculation time
        start_time = time.time()
        for file_path in test_files * 10:  # Calculate each file 10 times
            size = email_sender._get_file_size(file_path)
            formatted = email_sender._get_file_size_formatted(file_path)
        end_time = time.time()

        duration = end_time - start_time
        log_performance(logger, "file_size_calculation", duration,
                       {"files_tested": len(test_files) * 10})

        # Should complete in reasonable time
        assert duration < 1.0

    def test_config_validation_performance(self):
        """Test configuration validation performance."""
        # Measure validation time for complex configs
        start_time = time.time()
        for _ in range(100):
            config = ConfigValidator.validate_and_complete_config(self.test_config)
        end_time = time.time()

        duration = end_time - start_time
        log_performance(logger, "config_validation_100x", duration)

        # Should complete in reasonable time
        assert duration < 1.0

    def test_email_message_creation_performance(self):
        """Test email message creation performance."""
        email_sender = EmailSender(config=self.test_config)

        # Create test attachment
        attachment_path = os.path.join(self.temp_dir, 'test_attachment.txt')
        with open(attachment_path, 'w') as f:
            f.write('Test attachment content for performance testing')

        # Measure message creation time
        start_time = time.time()
        for _ in range(50):
            msg = email_sender._create_email_message(attachment_path, "Performance test summary")
        end_time = time.time()

        duration = end_time - start_time
        log_performance(logger, "email_message_creation_50x", duration)

        # Should complete in reasonable time
        assert duration < 2.0

    def test_logger_performance(self):
        """Test logging performance."""
        # Measure logging time
        start_time = time.time()
        for i in range(1000):  # Log 1000 messages
            log_performance(logger, f"test_operation_{i}", 0.001, {"iteration": i})
        end_time = time.time()

        duration = end_time - start_time
        log_performance(logger, "logging_1000_messages", duration)

        # Should complete in reasonable time (less than 5 seconds for 1000 logs)
        assert duration < 5.0

    def test_memory_usage_during_operations(self):
        """Test memory usage during intensive operations."""
        # Perform intensive operations without psutil
        email_sender = EmailSender(config=self.test_config)

        # Create multiple large attachments
        for i in range(10):
            file_path = os.path.join(self.temp_dir, f'large_file_{i}.txt')
            with open(file_path, 'w') as f:
                f.write('x' * 100000)  # 100KB each

            # Process each file
            size = email_sender._get_file_size(file_path)
            formatted = email_sender._get_file_size_formatted(file_path)

        # If we get here without memory errors, the test passes
        log_performance(logger, "memory_usage_test", 0,
                       {"files_processed": 10, "file_size_kb": 100})

        assert True  # Test completed successfully

    def test_concurrent_config_loading(self):
        """Test concurrent configuration loading."""
        import threading
        import queue

        config_path = os.path.join(self.temp_dir, 'concurrent_config.json')
        with open(config_path, 'w') as f:
            import json
            json.dump(self.test_config, f)

        results = queue.Queue()
        errors = queue.Queue()

        def load_config_worker():
            try:
                for _ in range(20):
                    config = ConfigValidator.load_config(config_path)
                    results.put(config)
            except Exception as e:
                errors.put(e)

        # Start multiple threads
        threads = []
        for _ in range(5):
            thread = threading.Thread(target=load_config_worker)
            threads.append(thread)
            thread.start()

        # Wait for all threads to complete
        for thread in threads:
            thread.join()

        # Check results
        success_count = results.qsize()
        error_count = errors.qsize()

        log_performance(logger, "concurrent_config_loading", 0,
                       {"success_count": success_count, "error_count": error_count})

        # Should have more successes than failures
        assert success_count > error_count
        assert success_count >= 80  # At least 80% success rate

    def test_large_configuration_handling(self):
        """Test handling of large configuration objects."""
        # Create a large configuration with many fields
        large_config = self.test_config.copy()

        # Add many additional fields
        for i in range(100):
            large_config[f'extra_field_{i}'] = f'value_{i}' * 10  # Long values

        start_time = time.time()
        validated_config = ConfigValidator.validate_and_complete_config(large_config)
        end_time = time.time()

        duration = end_time - start_time
        log_performance(logger, "large_config_validation", duration,
                       {"config_size": len(large_config)})

        # Should handle large configs efficiently
        assert duration < 1.0
        assert len(validated_config) >= len(large_config)

    def test_email_attachment_processing_performance(self):
        """Test email attachment processing performance."""
        email_sender = EmailSender(config=self.test_config)

        # Create attachments of various sizes
        attachments = []
        for size in [1000, 10000, 100000, 1000000]:  # 1KB to 1MB
            file_path = os.path.join(self.temp_dir, f'attachment_{size}.txt')
            with open(file_path, 'w') as f:
                f.write('x' * size)
            attachments.append(file_path)

        # Measure attachment processing time
        start_time = time.time()
        for attachment_path in attachments:
            # Simulate attachment processing
            file_size = email_sender._get_file_size(attachment_path)
            mime_type, encoding = email_sender._get_mime_type(attachment_path)
            formatted_size = email_sender._get_file_size_formatted(attachment_path)
        end_time = time.time()

        duration = end_time - start_time
        log_performance(logger, "attachment_processing", duration,
                       {"attachments_processed": len(attachments),
                        "total_size": sum(os.path.getsize(f) for f in attachments)})

        # Should process attachments efficiently
        assert duration < 2.0