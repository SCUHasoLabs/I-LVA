using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.IO;
using SimpleJSON;

public class PositionClassifier : MonoBehaviour
{
    public float scaleSpeed = 1f;

    //declaring struct that matches the db.json structure
    [System.Serializable] //ensures that content is serialized (converted into something unity knows)
    public class rawData
    {
        public int id;
        //public string name;
        //public int classification;
        public float diff_x;
        public float diff_z;
    }

    public class ClassificationData
    {
        public Vector3 position;
        public float diff_x;
        public float diff_z;
        //public int classification;
    }

    public List<ClassificationData> classy = new List<ClassificationData>();

    // Start is called before the first frame update
    private void Start()
    {
        LoadClassificationData("/Users/arianasun/Desktop/research/I-LVA/unity_json/db.json");
        MapPositionToClassification(transform.position);
    }
    

    //method to read classification data from JSON file
    public void LoadClassificationData(string filePath)
    {
        if (File.Exists(filePath))
        {
            //reads file and assigns everything into string json variable
            string json = File.ReadAllText(filePath);

            //clears whatever was previously in classy, start fresh          
            classy.Clear();

            //using SimpleJSON
            //assign rootNode to go through the json file
            JSONNode rootNode = JSON.Parse(json);

            Debug.Log(json);
            
            //since json file has various objects with arrays in each
            if (rootNode.IsObject)
            {
                Debug.Log("inside if statement for rootNode.IsObject");
                //have to get "rawData" array from root object
                JSONNode rawDataArray = rootNode["raw data"];

                Debug.Log("entering for loop for jsonnode node in rawdataarray");
                foreach (JSONNode node in rawDataArray)
                {
                    rawData data = new rawData
                    {
                        id = node["id"].AsInt,
                        //name = node["name"].Value,
                        //classification = node["classification"].AsInt,
                        diff_x = node["diff_x"].AsFloat,
                        diff_z = node["diff_y"].AsFloat
                    };

                    Debug.Log("printing emg data");
                    Debug.Log(data.id);
                    //Debug.Log(data.name);
                    //Debug.Log(data.classification);
                    Debug.Log(data.diff_x);
                    Debug.Log(data.diff_z);

                    ClassificationData classData = new ClassificationData
                    {
                        position = Vector3.zero,
                        diff_x = data.diff_x,
                        diff_z = data.diff_z
                        //classification = data.classification
                    };

                    Debug.Log("printing classData data");
                    Debug.Log(classData.position);
                    Debug.Log(classData.diff_x);
                    Debug.Log(classData.diff_z);
                    //Debug.Log(classData.classification);
                    

                    classy.Add(classData);
                }
                Debug.Log("exiting for loop from jsonnode node in rawdataaraay");
            } 
            else
            {
                Debug.LogError("Invalid JSON format. Expected an array. so sad :(((");
            }
        }
        else
        {
            Debug.LogError("awww JSON file not found at path: " + filePath);
            return;
        }
    }

    private IEnumerator MapPositionToClassification(Vector3 position)
    {

        if (classy == null)
        {
            Debug.LogWarning("classy is null. Make sure to load data before calling MapPositionToClassification.");
            yield return null;
        }

        foreach (var data in classy)
        {
            Debug.Log("entered for loop for data in classy yay");
            Debug.Log("entered if statement, continuing with changes yay");
            //Debug.Log("Classification: " + data.classification);

            Debug.Log("waiting for initial delay");
            yield return new WaitForSeconds(3);
            Debug.Log("starting position change now");
            
            //code to change positioning based off of difference in x and y values
            GameObject cube = GameObject.Find("Cube");

            if (cube != null)
            {
                //cube.transform.position += new Vector3(data.diff_x, data.z, 0);
                cube.transform.position += new Vector3(data.diff_x, 0, data.diff_z) * scaleSpeed * Time.deltaTime;
                Debug.Log("position changed yay");
            }
            else
            {
                Debug.LogWarning("cube not found in the scene.");
            }

        }
    }

    // Update is called once per frame
    private void Update()
    {
        
        if (classy != null)
        {
            StartCoroutine(MapPositionToClassification(transform.position));
        }
        
    }
}