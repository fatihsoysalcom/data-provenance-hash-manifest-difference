import hashlib
import json

def calculate_provenance_hash(data_content, manifest):
    """
    Calculates a hash that represents both the dataset content and its provenance manifest.
    This simulates a 'digital fingerprint' sensitive to both data and its description.
    """
    # Ensure consistent serialization for hashing
    # Sort keys for manifest to ensure consistent hash regardless of dict insertion order
    manifest_str = json.dumps(manifest, sort_keys=True, indent=None)
    
    # Combine data content and manifest string
    # For simplicity, data_content is assumed to be a list of strings.
    # Join them to form a single string representation of the data.
    data_str = "\n".join(data_content)
    
    combined_string = data_str + "\n" + manifest_str
    
    # Use SHA256 for hashing
    return hashlib.sha256(combined_string.encode('utf-8')).hexdigest()

def create_manifest(source, preprocessing_steps, version, description):
    """
    Creates a dictionary representing the provenance manifest for a dataset.
    """
    return {
        "source": source,
        "preprocessing_steps": preprocessing_steps,
        "version": version,
        "description": description
    }

def compare_manifests(manifest1, manifest2):
    """
    Compares two manifests and returns a dictionary of differences.
    This highlights the 'manifest difference' that explains a hash change.
    """
    diff = {}
    all_keys = set(manifest1.keys()).union(set(manifest2.keys()))
    for key in all_keys:
        val1 = manifest1.get(key)
        val2 = manifest2.get(key)
        if val1 != val2:
            diff[key] = {"old": val1, "new": val2}
    return diff

def main():
    print("--- Dataset Provenance and Hash Explanation ---")

    # --- Version 1: Initial Dataset and Manifest ---
    dataset_v1_content = [
        "record_id:1,name:Alice,age:30",
        "record_id:2,name:Bob,age:24",
        "record_id:3,name:Charlie,age:35"
    ]
    manifest_v1 = create_manifest(
        source="internal_crm_export",
        preprocessing_steps=["deduplication", "anonymization_names"],
        version="1.0",
        description="Customer data, names anonymized, duplicates removed."
    )
    
    hash_v1 = calculate_provenance_hash(dataset_v1_content, manifest_v1)
    print(f"\nVersion 1 Hash: {hash_v1}")
    print(f"Manifest V1: {json.dumps(manifest_v1, indent=2)}")

    # --- Version 2: Change in Data Content ---
    print("\n--- Scenario 1: Data Content Change ---")
    dataset_v2_content_changed = [
        "record_id:1,name:Alice,age:30",
        "record_id:2,name:Bob,age:24",
        "record_id:4,name:David,age:28" # Changed record 3 to 4
    ]
    # Manifest remains the same, but the underlying data changed
    manifest_v2_data_change = manifest_v1 
    
    hash_v2_data_change = calculate_provenance_hash(dataset_v2_content_changed, manifest_v2_data_change)
    print(f"Version 2 (Data Changed) Hash: {hash_v2_data_change}")
    
    if hash_v1 != hash_v2_data_change:
        print("Hash changed! (Expected, as data content was modified)")
        # When manifests are identical but hash differs, the change must be in the raw data.
        print("Manifests are identical, indicating the change is in the raw data content.")
        print(f"Manifest V1 == Manifest V2 (Data Changed): {manifest_v1 == manifest_v2_data_change}")
    else:
        print("Hash did not change (unexpected for data modification).")

    # --- Version 3: Change in Provenance/Manifest ---
    print("\n--- Scenario 2: Provenance/Manifest Change ---")
    # Data content remains the same as V1
    dataset_v3_provenance_change_content = dataset_v1_content 
    
    # Manifest changes: a new preprocessing step is added and version updated
    manifest_v3_provenance_changed = create_manifest(
        source="internal_crm_export",
        preprocessing_steps=["deduplication", "anonymization_names", "normalize_age_range"], # Added step
        version="1.1", # Version updated
        description="Customer data, names anonymized, duplicates removed, age normalized." # Description updated
    )
    
    hash_v3_provenance_changed = calculate_provenance_hash(dataset_v3_provenance_change_content, manifest_v3_provenance_changed)
    print(f"Version 3 (Provenance Changed) Hash: {hash_v3_provenance_changed}")

    if hash_v1 != hash_v3_provenance_changed:
        print("Hash changed! (Expected, as provenance manifest was modified)")
        # This is where the 'Manifest Farkı' (Manifest Difference) comes into play.
        # By comparing the manifests, we can explain *why* the hash changed.
        print("\n--- Explaining the Hash Difference (Manifest Comparison) ---")
        diff = compare_manifests(manifest_v1, manifest_v3_provenance_changed)
        if diff:
            print("Differences found in manifests:")
            for key, values in diff.items():
                print(f"  '{key}': Old='{values['old']}', New='{values['new']}'")
        else:
            print("No differences found in manifests (this would be unexpected if hash changed).")
    else:
        print("Hash did not change (unexpected for manifest modification).")

    # --- Version 4: No Change (should have same hash as V1) ---
    print("\n--- Scenario 3: No Change ---")
    dataset_v4_no_change_content = dataset_v1_content
    manifest_v4_no_change = manifest_v1

    hash_v4_no_change = calculate_provenance_hash(dataset_v4_no_change_content, manifest_v4_no_change)
    print(f"Version 4 (No Change) Hash: {hash_v4_no_change}")

    if hash_v1 == hash_v4_no_change:
        print("Hash is identical to V1. (Expected, as neither data nor manifest changed)")
    else:
        print("Hash changed unexpectedly.")

if __name__ == "__main__":
    main()
